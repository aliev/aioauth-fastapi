from sqlalchemy.ext.asyncio import create_async_engine
import aioredis
from aioauth_fastapi.storage import db, redis
from aioauth_fastapi.config import settings


async def create_postgresql_connection():
    db.sqlalchemy_engine = create_async_engine(settings.PSQL_DSN, echo=True)


async def close_postgresql_connection():
    if db.sqlalchemy_engine is not None:
        await db.sqlalchemy_engine.dispose()


async def create_redis_connection():
    redis.redis_pool = aioredis.from_url(settings.REDIS_DSN)


async def close_redis_connection():
    if redis.redis_pool is not None:
        await redis.redis_pool.close()


on_startup = [
    create_postgresql_connection,
    create_redis_connection,
]
on_shutdown = [
    close_postgresql_connection,
    close_redis_connection,
]
