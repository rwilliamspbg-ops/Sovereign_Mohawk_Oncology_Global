import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from .wal_ledger import WriteAheadLedger


class AuditLogger:
    def __init__(
        self,
        file_path: str,
        forwarder: Any = None,
        wal_path: Optional[str] = None,
        enable_wal: bool = True,
    ) -> None:
        self.file_path = file_path
        self.forwarder = forwarder
        self.wal = (
            WriteAheadLedger(wal_path or f"{file_path}.wal") if enable_wal else None
        )

    def log(self, event_type: str, payload: Dict[str, Any]) -> None:
        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "payload": payload,
        }
        if self.wal is not None:
            self.wal.append(
                event_type=event_type,
                payload=payload,
                ts=record["ts"],
            )
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, sort_keys=True) + "\n")
        if self.forwarder is not None:
            try:
                self.forwarder.forward(record)
            except Exception:
                # Fail closed for policy checks, but fail open for SIEM transport.
                pass
