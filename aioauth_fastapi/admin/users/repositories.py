from typing import List
from sqlalchemy.sql.expression import delete, select, update
from aioauth_fastapi.storage.db import Database
from aioauth_fastapi.users.models import User
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError
from aioauth_fastapi.storage.exceptions import ObjectDoesNotExist, ObjectExist


class UserAdminRepository:
    def __init__(self, database: Database):
        self.database = database

    async def user_create(self, user: User) -> User:

        try:
            await self.database.add(user)
        except IntegrityError:
            raise ObjectExist

        return user

    async def user_details(self, id: UUID4) -> User:
        results = await self.database.select(select(User).where(User.id == id))

        user = results.one_or_none()

        if user is None:
            raise ObjectDoesNotExist

        return user

    async def users_list(self) -> List[User]:
        q_results = await self.database.select(select(User))

        return q_results.fetchall()

    async def user_delete(self, id: UUID4) -> None:
        await self.database.delete(delete(User).where(User.id == id))

    async def user_update(self, id: UUID4, user: User) -> User:
        try:
            await self.database.update(
                update(User)
                .where(User.id == id)
                .values(**user.dict(exclude={"id": True}))
            )
        except IntegrityError:
            raise ObjectExist

        return user
