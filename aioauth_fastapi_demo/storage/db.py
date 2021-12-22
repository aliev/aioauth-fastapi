from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.expression import Delete, Update
from sqlalchemy.pool import NullPool


class PostgreSQL:
    def __init__(self, dsn: str) -> None:
        # NOTE: https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#using-multiple-asyncio-event-loops
        self.engine = create_async_engine(dsn, echo=True, poolclass=NullPool)
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

    async def select(self, q: Select) -> ScalarResult:
        async with self.session() as session:
            results = await session.execute(q)
            return results.scalars()

    async def add(self, model) -> None:
        async with self.session() as session:
            session.add(model)
            await session.commit()

    async def delete(self, q: Delete) -> None:
        async with self.session() as session:
            await session.execute(q)
            await session.commit()

    async def update(self, q: Update):
        async with self.session() as session:
            await session.execute(q)
            await session.commit()
