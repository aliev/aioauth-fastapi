from fastapi import Request
from pydantic.types import UUID4
from .models import UserCreate
from aioauth_fastapi.users.models import User
from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from .repositories import UserAdminRepository


class UserAdminService:
    def __init__(self, users_admin_repository: "UserAdminRepository") -> None:
        self.repository = users_admin_repository

    async def user_create(self, *, request: Request, body: UserCreate) -> User:
        ...

    async def user_details(self, *, request: Request, id: UUID4) -> User:
        ...

    async def users_list(self, *, request: Request) -> List[User]:
        ...

    async def user_delete(self, *, request: Request, id: UUID4) -> None:
        ...

    async def user_update(self, *, request: Request, id: UUID4) -> User:
        ...
