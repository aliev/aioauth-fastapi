from typing import List, Optional
from sqlalchemy.sql.expression import delete, select, update
from aioauth_fastapi.storage.db import Database
from aioauth_fastapi.users.models import User
from pydantic import UUID4


class UserAdminRepository:
    def __init__(self, database: Database):
        self.database = database

    async def user_create(self, user: User) -> User:
        await self.database.add(user)
        return user

    async def user_details(self, id: UUID4) -> Optional[User]:
        results = await self.database.select(select(User).where(User.id == id))

        return results.one_or_none()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        results = await self.database.select(
            select(User).where(User.username == username)
        )
        return results.one_or_none()

    async def users_list(self) -> List[User]:
        q_results = await self.database.select(select(User))

        return q_results.fetchall()

    async def user_delete(self, id: UUID4) -> None:
        await self.database.delete(delete(User).where(User.id == id))

    async def user_update(self, id: UUID4, user: User) -> User:
        await self.database.update(
            update(User).where(User.id == id).values(**user.dict(exclude={"id": True}))
        )

        return user
