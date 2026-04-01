import os
import tempfile
import unittest

from security_wrapper.nonce_store import InMemoryNonceStore, SqliteNonceStore


class TestNonceStore(unittest.TestCase):
    def test_inmemory_store(self):
        store = InMemoryNonceStore()
        self.assertFalse(store.seen(1, "n-1"))
        store.add(1, "n-1")
        self.assertTrue(store.seen(1, "n-1"))

    def test_sqlite_store(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "nonce.db")
            store = SqliteNonceStore(db_path)
            self.assertFalse(store.seen(2, "n-2"))
            store.add(2, "n-2")

            # Re-open to confirm persistence across restarts.
            store2 = SqliteNonceStore(db_path)
            self.assertTrue(store2.seen(2, "n-2"))


if __name__ == "__main__":
    unittest.main()
