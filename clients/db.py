import asyncpg


class AsyncDBClient:
    def __init__(self, dsn: str, min_size: int = 1, max_size: int = 10):
        self.dsn = dsn
        self.pool: asyncpg.Pool | None = None
        self.min_size = min_size
        self.max_size = max_size

    async def connect(self):
        if self.pool is None:
            self.pool = await asyncpg.create_pool(
                dsn=self.dsn,
                min_size=self.min_size,
                max_size=self.max_size
            )

    async def close(self):
        if self.pool:
            await self.pool.close()
            self.pool = None

    async def fetch_count(self, value: str) -> int:
        async with self.pool.acquire() as conn:
            return await conn.fetchval(
                'SELECT count(*) FROM my_table WHERE some_col=$1',
                value
            )

    async def insert_row(self, col1: str, col2: str) -> None:
        async with self.pool.acquire() as conn:
            await conn.execute(
                'INSERT INTO my_table (col1, col2) VALUES ($1, $2)',
                col1,
                col2
            )
