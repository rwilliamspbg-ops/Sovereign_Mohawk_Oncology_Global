import json
import os
import threading
import zlib
from dataclasses import dataclass
from hashlib import sha256
from typing import Any, Dict, Iterable, List, Optional


class WALIntegrityError(RuntimeError):
    pass


@dataclass(frozen=True)
class WALRecord:
    version: int
    index: int
    ts: str
    event_type: str
    payload: Dict[str, Any]
    prev_hash: str
    record_hash: str
    crc32: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "v": self.version,
            "index": self.index,
            "ts": self.ts,
            "event_type": self.event_type,
            "payload": self.payload,
            "prev_hash": self.prev_hash,
            "record_hash": self.record_hash,
            "crc32": self.crc32,
        }


class WriteAheadLedger:
    """Append-only WAL with hash-chain + CRC integrity checks."""

    VERSION = 1

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self._lock = threading.Lock()
        self._last_hash = ""
        self._next_index = 1
        self._bootstrap_state()

    def append(
        self, event_type: str, payload: Dict[str, Any], ts: str
    ) -> Dict[str, Any]:
        with self._lock:
            record = self._build_record(
                index=self._next_index,
                ts=ts,
                event_type=event_type,
                payload=payload,
                prev_hash=self._last_hash,
            )
            raw = (
                json.dumps(
                    record.to_dict(), sort_keys=True, separators=(",", ":")
                ).encode("utf-8")
                + b"\n"
            )
            self._append_bytes(raw)
            self._last_hash = record.record_hash
            self._next_index += 1
            return record.to_dict()

    def replay(self, strict: bool = True) -> List[Dict[str, Any]]:
        records: List[Dict[str, Any]] = []
        for rec in self._iter_verified_records(strict=strict):
            records.append(rec.to_dict())
        return records

    def _bootstrap_state(self) -> None:
        if not os.path.exists(self.file_path):
            return
        last: Optional[WALRecord] = None
        for rec in self._iter_verified_records(strict=False):
            last = rec
        if last is None:
            return
        self._last_hash = last.record_hash
        self._next_index = last.index + 1

    def _iter_verified_records(self, strict: bool) -> Iterable[WALRecord]:
        if not os.path.exists(self.file_path):
            return

        expected_index = 1
        expected_prev_hash = ""

        with open(self.file_path, "r", encoding="utf-8") as f:
            for line_num, raw_line in enumerate(f, start=1):
                line = raw_line.strip()
                if not line:
                    continue

                try:
                    data = json.loads(line)
                except json.JSONDecodeError as exc:
                    if strict:
                        raise WALIntegrityError(
                            f"invalid JSON frame at line {line_num}"
                        ) from exc
                    break

                try:
                    record = self._parse_record(data)
                    self._verify_record(record, expected_index, expected_prev_hash)
                except WALIntegrityError:
                    if strict:
                        raise
                    break

                yield record
                expected_index += 1
                expected_prev_hash = record.record_hash

    def _append_bytes(self, data: bytes) -> None:
        parent = os.path.dirname(self.file_path)
        if parent:
            os.makedirs(parent, exist_ok=True)

        flags = os.O_CREAT | os.O_APPEND | os.O_WRONLY
        fd = os.open(self.file_path, flags, 0o644)
        try:
            os.write(fd, data)
            os.fsync(fd)
        finally:
            os.close(fd)

    def _build_record(
        self,
        index: int,
        ts: str,
        event_type: str,
        payload: Dict[str, Any],
        prev_hash: str,
    ) -> WALRecord:
        core = {
            "v": self.VERSION,
            "index": index,
            "ts": ts,
            "event_type": event_type,
            "payload": payload,
            "prev_hash": prev_hash,
        }
        core_bytes = json.dumps(core, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
        record_hash = sha256(core_bytes).hexdigest()
        crc32 = zlib.crc32(core_bytes) & 0xFFFFFFFF
        return WALRecord(
            version=self.VERSION,
            index=index,
            ts=ts,
            event_type=event_type,
            payload=payload,
            prev_hash=prev_hash,
            record_hash=record_hash,
            crc32=crc32,
        )

    def _parse_record(self, data: Dict[str, Any]) -> WALRecord:
        try:
            return WALRecord(
                version=int(data["v"]),
                index=int(data["index"]),
                ts=str(data["ts"]),
                event_type=str(data["event_type"]),
                payload=dict(data["payload"]),
                prev_hash=str(data["prev_hash"]),
                record_hash=str(data["record_hash"]),
                crc32=int(data["crc32"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise WALIntegrityError("missing or invalid WAL fields") from exc

    def _verify_record(
        self, record: WALRecord, expected_index: int, expected_prev_hash: str
    ) -> None:
        if record.version != self.VERSION:
            raise WALIntegrityError(f"unsupported WAL version: {record.version}")
        if record.index != expected_index:
            raise WALIntegrityError(
                f"index gap or reordering at {record.index}, expected {expected_index}"
            )
        if record.prev_hash != expected_prev_hash:
            raise WALIntegrityError("hash-chain mismatch")

        rebuilt = self._build_record(
            index=record.index,
            ts=record.ts,
            event_type=record.event_type,
            payload=record.payload,
            prev_hash=record.prev_hash,
        )
        if record.record_hash != rebuilt.record_hash:
            raise WALIntegrityError("record hash mismatch")
        if record.crc32 != rebuilt.crc32:
            raise WALIntegrityError("crc32 mismatch")
