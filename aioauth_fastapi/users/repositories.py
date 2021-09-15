from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from aioauth_fastapi.storage.db import Database

from ..users.models import User
from .exceptions import DuplicateUserException


class UserRepository:
    def __init__(self, database: Database):
        self.database = database

    async def get_user(self, username: str) -> Optional[User]:
        q = select(User).where(User.username == username)

        async with self.database.session() as session:
            results = await session.execute(q)
            return results.scalars().one_or_none()

    async def create_user(self, **kwargs) -> None:
        user = User(**kwargs)
        user.set_password(kwargs.get("password"))

        async with self.database.session() as session:
            session.add(user)

            try:
                await session.commit()
            except IntegrityError:
                raise DuplicateUserException
