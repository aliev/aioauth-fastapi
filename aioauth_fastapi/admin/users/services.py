from fastapi import Request, HTTPException, status
from pydantic.types import UUID4
from .models import UserCreate
from aioauth_fastapi.users.models import User
from aioauth_fastapi.storage.exceptions import ObjectExist, ObjectDoesNotExist
from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from .repositories import UserAdminRepository


class UserAdminService:
    def __init__(self, users_admin_repository: "UserAdminRepository") -> None:
        self.repository = users_admin_repository

    async def user_create(self, *, request: Request, body: UserCreate) -> User:
        user = User(
            is_superuser=body.is_superuser,
            is_blocked=body.is_blocked,
            is_active=body.is_active,
            username=body.username,
        )

        user.set_password(body.password)

        try:
            return await self.repository.user_create(user)
        except ObjectExist:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="User already exists",
            )

    async def user_details(self, *, request: Request, id: UUID4) -> User:

        try:
            return await self.repository.user_details(id)
        except ObjectDoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

    async def users_list(self, *, request: Request) -> List[User]:
        return await self.repository.users_list()

    async def user_delete(self, *, request: Request, id: UUID4) -> None:
        ...

    async def user_update(self, *, request: Request, id: UUID4) -> User:
        ...
