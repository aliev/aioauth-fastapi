from aioauth_fastapi.storage.db import Storage
from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from .exceptions import DuplicateUserException

from ..storage.tables import UserTable


class UserRepository:
    def __init__(self, storage: Storage):
        self.storage = storage

    async def get_user(self, username: str) -> Optional[UserTable]:
        q = select(UserTable).where(UserTable.username == username)

        async with self.storage.session() as session:
            results = await session.execute(q)
            return results.scalars().one_or_none()

    async def create_user(self, **kwargs) -> None:
        user = UserTable(**kwargs)

        async with self.storage.session() as session:
            session.add(user)

            try:
                await session.commit()
            except IntegrityError:
                raise DuplicateUserException
