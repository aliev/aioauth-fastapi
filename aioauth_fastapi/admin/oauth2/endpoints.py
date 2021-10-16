from typing import List, Optional
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Request
from fastapi.params import Depends
from pydantic import UUID4

from aioauth_fastapi.admin.oauth2.services import Oauth2AdminService
from .models import ClientCreate, ClientUpdate
from ...containers import ApplicationContainer
from ...oauth2.models import Client

routers = APIRouter()


@routers.post("/", response_model=Client)
@inject
async def client_create(
    request: Request,
    body: ClientCreate,
    service: Oauth2AdminService = Depends(
        Provide[ApplicationContainer.admin_package.oauth2_admin_service]
    ),
) -> Client:
    return await service.client_create(request=request, body=body)


@routers.get("/{id}/", response_model=Client)
@inject
async def client_details(
    request: Request,
    id: UUID4,
    service: Oauth2AdminService = Depends(
        Provide[ApplicationContainer.admin_package.oauth2_admin_service]
    ),
) -> Client:
    return await service.client_details(request=request, id=id)


@routers.get("/", response_model=List[Client])
@inject
async def client_list(
    request: Request,
    service: Oauth2AdminService = Depends(
        Provide[ApplicationContainer.admin_package.oauth2_admin_service]
    ),
) -> Optional[List[Client]]:
    return await service.client_list(request=request)


@routers.delete("/{id}/")
@inject
async def client_delete(
    request: Request,
    id: UUID4,
    service: Oauth2AdminService = Depends(
        Provide[ApplicationContainer.admin_package.oauth2_admin_service]
    ),
):
    return await service.client_delete(request=request, id=id)


@routers.patch("/{id}/", response_model=Client)
@inject
async def client_update(
    request: Request,
    body: ClientUpdate,
    id: UUID4,
    service: Oauth2AdminService = Depends(
        Provide[ApplicationContainer.admin_package.oauth2_admin_service]
    ),
) -> Client:
    return await service.client_update(request=request, body=body, id=id)
