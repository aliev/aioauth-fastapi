from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from aioauth_fastapi.storage.db import Database

from ..users.models import User
from .exceptions import DuplicateUserException


class UserRepository:
    def __init__(self, database: Database):
        self.database = database

    async def get_user(self, username: str) -> Optional[User]:
        q_results = await self.database.select(
            select(User)
            .options(
                # for relationship loading, eager loading should be applied.
                selectinload(User.user_tokens)
            )
            .where(User.username == username)
        )

        return q_results.one_or_none()

    async def create_user(self, **kwargs) -> None:
        user = User(**kwargs)
        user.set_password(kwargs.get("password"))

        try:
            await self.database.add(user)
        except IntegrityError:
            raise DuplicateUserException
