import aioredis
from ..config import settings


async def init_redis_pool():
    pool = aioredis.from_url(settings.REDIS_DSN)
    yield pool
    await pool.close()


class Redis:
    def __init__(self, redis) -> None:
        self.redis = redis
