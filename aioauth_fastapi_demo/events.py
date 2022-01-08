from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlmodel.ext.asyncio.session import AsyncSession

from .config import settings
from .storage import sqlalchemy


async def create_sqlalchemy_connection():
    # NOTE: https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#using-multiple-asyncio-event-loops
    engine = create_async_engine(settings.PSQL_DSN, echo=True, poolclass=NullPool)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    sqlalchemy.sqlalchemy_session = async_session()


async def close_sqlalchemy_connection():
    if sqlalchemy.sqlalchemy_session is not None:
        await sqlalchemy.sqlalchemy_session.close()


on_startup = [
    create_sqlalchemy_connection,
]
on_shutdown = [
    close_sqlalchemy_connection,
]
