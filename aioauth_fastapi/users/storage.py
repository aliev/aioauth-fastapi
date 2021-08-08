from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import DuplicateUserException

from ..storage.tables import UserTable


class UserStorage:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self, username: str) -> Optional[UserTable]:
        q = select(UserTable).where(UserTable.username == username)
        results = await self.session.execute(q)

        return results.scalars().one_or_none()

    async def create_user(self, **kwargs) -> None:
        user = UserTable(**kwargs)
        self.session.add(user)

        try:
            await self.session.commit()
        except IntegrityError:
            raise DuplicateUserException
