from psycopg_pool import ConnectionPool


class PostgresClient:
    def __init__(self, dsn: str, min_size: int = 1, max_size: int = 10):
        self.dsn: str = dsn
        self.pool: ConnectionPool | None = None
        self.min_size: int = min_size
        self.max_size: int = max_size

    def connect(self):
        if self.pool is None:
            self.pool = ConnectionPool(
                self.dsn,
                min_size=self.min_size,
                max_size=self.max_size,
                timeout=30,
            )

    def close(self):
        if self.pool:
            self.pool.close()
            self.pool = None

    def fetch_count(self, value: str) -> int:
        with self.pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) FROM logs WHERE message=%s", (value,)
                )
                result = cursor.fetchone()
                return result[0]

    def insert_row(self, message: str) -> None:
        with self.pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO logs (message, timestamp) VALUES (%s, NOW())",
                    (message,),
                )
                conn.commit()
