from typing import List
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Request
from fastapi.params import Depends
from pydantic.types import UUID4

from aioauth_fastapi.admin.users.services import UserAdminService
from aioauth_fastapi.containers import ApplicationContainer
from aioauth_fastapi.users.models import User
from .models import UserCreate

routers = APIRouter()


@routers.post("/", response_model=User)
@inject
async def user_create(
    request: Request,
    body: UserCreate,
    service: UserAdminService = Depends(
        Provide[ApplicationContainer.admin_package.user_admin_service]
    ),
) -> User:
    return await service.user_create(request=request, body=body)


@routers.get("/{id}/", response_model=User)
@inject
async def user_details(
    request: Request,
    id: UUID4,
    service: UserAdminService = Depends(
        Provide[ApplicationContainer.admin_package.user_admin_service]
    ),
) -> User:
    return await service.user_details(request=request, id=id)


@routers.get("/", response_model=List[User])
async def users_list(
    request: Request,
    id: UUID4,
    service: UserAdminService = Depends(
        Provide[ApplicationContainer.admin_package.user_admin_service]
    ),
) -> List[User]:
    return await service.users_list(request=request)


@routers.get("/{id}/")
async def user_delete(
    request: Request,
    id: UUID4,
    service: UserAdminService = Depends(
        Provide[ApplicationContainer.admin_package.user_admin_service]
    ),
):
    return await service.user_delete(request=request, id=id)


@routers.patch("/{id}/", response_model=User)
async def user_update(
    request: Request,
    id: UUID4,
    service: UserAdminService = Depends(
        Provide[ApplicationContainer.admin_package.user_admin_service]
    ),
) -> User:
    return await service.user_update(request=request, id=id)
