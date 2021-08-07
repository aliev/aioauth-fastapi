from typing import Optional
from aioredis.client import Redis

redis_pool: Optional[Redis] = None


def get_redis_pool() -> Optional[Redis]:
    return redis_pool
