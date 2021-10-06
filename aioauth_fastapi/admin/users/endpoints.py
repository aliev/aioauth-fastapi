from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter
from fastapi.params import Depends

from aioauth_fastapi.admin.users.services import UserAdminService
from aioauth_fastapi.containers import ApplicationContainer

routers = APIRouter()


@routers.get("/")
@inject
async def users(
    user_admin_service: UserAdminService = Depends(
        Provide[ApplicationContainer.admin_package.user_admin_service]
    ),
):
    ...
