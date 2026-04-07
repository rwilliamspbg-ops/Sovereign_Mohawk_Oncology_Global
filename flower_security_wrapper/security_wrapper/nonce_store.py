import sqlite3
from dataclasses import dataclass
from typing import Set, Tuple


class NonceStore:
    def seen(self, server_round: int, nonce: str) -> bool:
        raise NotImplementedError

    def add(self, server_round: int, nonce: str) -> None:
        raise NotImplementedError


@dataclass
class InMemoryNonceStore(NonceStore):
    values: Set[Tuple[int, str]]

    def __init__(self) -> None:
        self.values = set()

    def seen(self, server_round: int, nonce: str) -> bool:
        return (server_round, nonce) in self.values

    def add(self, server_round: int, nonce: str) -> None:
        self.values.add((server_round, nonce))


class SqliteNonceStore(NonceStore):
    def __init__(self, db_path: str = "nonce_cache.db") -> None:
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS seen_nonces (
                    server_round INTEGER NOT NULL,
                    nonce TEXT NOT NULL,
                    PRIMARY KEY (server_round, nonce)
                )
                """)
            conn.commit()

    def seen(self, server_round: int, nonce: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                "SELECT 1 FROM seen_nonces WHERE server_round = ? AND nonce = ?",
                (server_round, nonce),
            )
            return cur.fetchone() is not None

    def add(self, server_round: int, nonce: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR IGNORE INTO seen_nonces(server_round, nonce) VALUES (?, ?)",
                (server_round, nonce),
            )
            conn.commit()


class RedisNonceStore(NonceStore):
    def __init__(
        self, redis_url: str = "redis://localhost:6379/0", key_prefix: str = "nonce"
    ) -> None:
        try:
            import redis  # type: ignore
        except ImportError as exc:
            raise RuntimeError("redis package is required for RedisNonceStore") from exc

        self._client = redis.from_url(redis_url)
        self.key_prefix = key_prefix

    def _key(self, server_round: int, nonce: str) -> str:
        return f"{self.key_prefix}:{server_round}:{nonce}"

    def seen(self, server_round: int, nonce: str) -> bool:
        return bool(self._client.exists(self._key(server_round, nonce)))

    def add(self, server_round: int, nonce: str) -> None:
        self._client.set(self._key(server_round, nonce), "1")


class PostgresNonceStore(NonceStore):
    def __init__(self, dsn: str, table_name: str = "seen_nonces") -> None:
        try:
            import psycopg  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "psycopg package is required for PostgresNonceStore"
            ) from exc

        self._psycopg = psycopg
        self.dsn = dsn
        self.table_name = table_name
        self._init_db()

    def _init_db(self) -> None:
        with self._psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.table_name} (
                        server_round INTEGER NOT NULL,
                        nonce TEXT NOT NULL,
                        PRIMARY KEY (server_round, nonce)
                    )
                    """)
            conn.commit()

    def seen(self, server_round: int, nonce: str) -> bool:
        with self._psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT 1 FROM {self.table_name} WHERE server_round = %s AND nonce = %s",
                    (server_round, nonce),
                )
                return cur.fetchone() is not None

    def add(self, server_round: int, nonce: str) -> None:
        with self._psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"INSERT INTO {self.table_name}(server_round, nonce) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (server_round, nonce),
                )
            conn.commit()
