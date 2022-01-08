from typing import Optional

from sqlalchemy.engine.result import Result
from sqlalchemy.sql.expression import Delete, Update
from sqlalchemy.sql.selectable import Select
from sqlmodel.ext.asyncio.session import AsyncSession


class SQLAlchemyTransaction:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def __aenter__(self) -> "SQLAlchemyTransaction":
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

        await self.close()

    async def rollback(self):
        await self.session.rollback()

    async def commit(self):
        await self.session.commit()

    async def close(self):
        await self.session.close()


class SQLAlchemyStorage:
    def __init__(
        self, session: AsyncSession, transaction: SQLAlchemyTransaction
    ) -> None:
        self.session = session
        self.transaction = transaction

    async def select(self, q: Select) -> Result:
        async with self.transaction:
            return await self.session.execute(q)

    async def add(self, model) -> None:
        async with self.transaction:
            self.session.add(model)

    async def delete(self, q: Delete) -> None:
        async with self.transaction:
            await self.session.execute(q)

    async def update(self, q: Update):
        async with self.transaction:
            await self.session.execute(q)


sqlalchemy_session: Optional[AsyncSession] = None


def get_sqlalchemy_storage() -> SQLAlchemyStorage:
    """Get SQLAlchemy storage instance.

    Returns:
        SQLAlchemyStorage: SQLAlchemy storage instance
    """
    sqllachemy_trancation = SQLAlchemyTransaction(session=sqlalchemy_session)
    return SQLAlchemyStorage(
        session=sqlalchemy_session, transaction=sqllachemy_trancation
    )
