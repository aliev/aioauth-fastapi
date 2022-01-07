from typing import Optional
from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.expression import Delete, Update
from sqlmodel.ext.asyncio.session import AsyncSession


class SQLAlchemy:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

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


sqlalchemy_session: Optional[AsyncSession] = None


def get_database():
    return SQLAlchemy(session=sqlalchemy_session)
