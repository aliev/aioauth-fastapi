from fastapi import Request, HTTPException, status
from pydantic.types import UUID4
from .models import UserCreate, UserUpdate
from aioauth_fastapi.users.models import User
from typing import TYPE_CHECKING, List, Optional


if TYPE_CHECKING:
    from .repositories import UserAdminRepository


class UserAdminService:
    def __init__(self, users_admin_repository: "UserAdminRepository") -> None:
        self.repository = users_admin_repository

    async def user_create(self, *, request: Request, body: UserCreate) -> User:
        user_exists = await self.repository.get_user_by_username(body.username)

        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username already exists",
            )

        user = User(
            is_superuser=body.is_superuser,
            is_blocked=body.is_blocked,
            is_active=body.is_active,
            username=body.username,
        )

        user.set_password(body.password)

        return await self.repository.user_create(user)

    async def user_details(self, *, request: Request, id: UUID4) -> Optional[User]:

        user = await self.repository.user_details(id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

    async def users_list(self, *, request: Request) -> List[User]:
        return await self.repository.users_list()

    async def user_delete(self, *, request: Request, id: UUID4) -> None:
        await self.repository.user_delete(id)

    async def user_update(
        self, *, request: Request, body: UserUpdate, id: UUID4
    ) -> User:

        if body.username:
            user_exists = await self.repository.get_user_by_username(body.username)

            if user_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this username already exists",
                )

        user = User(id=id, **body.dict(exclude_unset=True, exclude={"password"}))

        if body.password is not None:
            user.set_password(body.password)

        return await self.repository.user_update(id, user)
