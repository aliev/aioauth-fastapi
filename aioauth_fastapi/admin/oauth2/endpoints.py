from typing import List
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Request
from fastapi.params import Depends, Query
from pydantic import UUID4

from aioauth_fastapi.admin.oauth2.services import Oauth2AdminService
from .models import ClientCreate
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
    page: int = Query(1),
    page_size: int = Query(10),
) -> List[Client]:
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
