import json
import os
import tempfile
import unittest

from security_wrapper.audit import AuditLogger
from security_wrapper.wal_ledger import WALIntegrityError, WriteAheadLedger


class TestWriteAheadLedger(unittest.TestCase):
    def test_append_and_replay(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            wal_path = os.path.join(tmpdir, "audit.wal")
            ledger = WriteAheadLedger(wal_path)

            ledger.append("event_a", {"k": 1}, ts="2026-01-01T00:00:00+00:00")
            ledger.append("event_b", {"k": 2}, ts="2026-01-01T00:00:01+00:00")

            rows = ledger.replay(strict=True)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["index"], 1)
            self.assertEqual(rows[1]["index"], 2)
            self.assertEqual(rows[1]["prev_hash"], rows[0]["record_hash"])

    def test_detects_tamper(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            wal_path = os.path.join(tmpdir, "audit.wal")
            ledger = WriteAheadLedger(wal_path)
            ledger.append("event_a", {"k": 1}, ts="2026-01-01T00:00:00+00:00")

            with open(wal_path, "r", encoding="utf-8") as f:
                row = json.loads(f.readline())
            row["payload"] = {"k": 999}
            with open(wal_path, "w", encoding="utf-8") as f:
                f.write(json.dumps(row, sort_keys=True) + "\n")

            with self.assertRaises(WALIntegrityError):
                ledger.replay(strict=True)

    def test_non_strict_recovers_after_partial_tail_write(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            wal_path = os.path.join(tmpdir, "audit.wal")
            ledger = WriteAheadLedger(wal_path)
            ledger.append("event_a", {"k": 1}, ts="2026-01-01T00:00:00+00:00")

            with open(wal_path, "a", encoding="utf-8") as f:
                f.write('{"invalid":')

            rows = ledger.replay(strict=False)
            self.assertEqual(len(rows), 1)

            with self.assertRaises(WALIntegrityError):
                ledger.replay(strict=True)


class TestAuditLoggerWithWal(unittest.TestCase):
    def test_writes_jsonl_and_wal(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            audit_path = os.path.join(tmpdir, "security_audit.jsonl")
            wal_path = os.path.join(tmpdir, "security_audit.wal")
            logger = AuditLogger(audit_path, wal_path=wal_path)

            logger.log("update_accepted", {"client_id": "hospital-eu-01", "round": 7})

            with open(audit_path, "r", encoding="utf-8") as f:
                line = f.readline()
                self.assertIn("update_accepted", line)

            replay = logger.wal.replay(strict=True)
            self.assertEqual(len(replay), 1)
            self.assertEqual(replay[0]["event_type"], "update_accepted")
            self.assertEqual(replay[0]["payload"]["round"], 7)


if __name__ == "__main__":
    unittest.main()
