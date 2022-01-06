from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.expression import Delete, Update
from sqlalchemy.pool import NullPool


class SQLAlchemy:
    def __init__(self, dsn: str) -> None:
        # NOTE: https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#using-multiple-asyncio-event-loops
        self.engine = create_async_engine(dsn, echo=True, poolclass=NullPool)
        async_session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )
        self.session = async_session()

    # @asynccontextmanager
    # async def session(self):
    #     async with self.async_session() as session:
    #         async with session.begin():
    #             try:
    #                 yield session
    #             except Exception:
    #                 await session.rollback()
    #                 raise
    #             finally:
    #                 await session.close()

    async def select(self, q: Select) -> ScalarResult:
        results = await self.session.execute(q)
        await self.session.close()
        return results.scalars()

    async def add(self, model) -> None:
        self.session.add(model)
        await self.session.commit()
        await self.session.close()

    async def delete(self, q: Delete) -> None:
        await self.session.execute(q)
        await self.session.commit()
        await self.session.close()

    async def update(self, q: Update):
        await self.session.execute(q)
        await self.session.commit()
        await self.session.close()
