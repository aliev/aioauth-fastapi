from typing import Optional
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from contextlib import asynccontextmanager


sqlalchemy_engine: Optional[AsyncEngine] = None


def get_sqlalchemy_async_session() -> sessionmaker:
    async_session = sessionmaker(
        sqlalchemy_engine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session


class Storage:
    def __init__(self, dsn: str) -> None:
        self.engine = create_async_engine(dsn, echo=True)
        self.async_session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    @asynccontextmanager
    async def session(self):
        async with self.async_session() as session:
            async with session.begin():
                try:
                    yield session
                except Exception:
                    await session.rollback()
                    raise
                finally:
                    await session.close()
