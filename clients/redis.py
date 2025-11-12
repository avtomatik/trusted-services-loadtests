import redis.asyncio as redis


class AsyncRedisClient:
    def __init__(self, url: str):
        self.url = url
        self.redis: redis.Redis | None = None

    async def connect(self):
        if self.redis is None:
            self.redis = redis.from_url(self.url, decode_responses=True)

    async def close(self):
        if self.redis:
            await self.redis.close()
            self.redis = None

    async def set_key(self, key: str, value: str, expire: int = 60):
        await self.redis.set(key, value, ex=expire)

    async def get_key(self, key: str):
        return await self.redis.get(key)
