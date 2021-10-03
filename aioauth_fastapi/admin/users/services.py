from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .repositories import UserAdminRepository


class UserAdminService:
    def __init__(self, users_admin_repository: "UserAdminRepository") -> None:
        self.repository = users_admin_repository
