import redis.asyncio as redis


class RedisClient:
    def __init__(self, url: str):
        self.url = url
        self.redis: redis.Redis | None = None

    def connect(self):
        if self.redis is None:
            self.redis = redis.from_url(self.url, decode_responses=True)

    def close(self):
        if self.redis:
            self.redis.close()
            self.redis = None

    def set_key(self, key: str, value: str, expire: int = 60):
        self.redis.set(key, value, ex=expire)

    def get_key(self, key: str):
        return self.redis.get(key)
