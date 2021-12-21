from typing import List, Optional
from dependency_injector.wiring import Provide, inject
from fastapi import Request, HTTPException, status, APIRouter
from fastapi.params import Depends
from pydantic import UUID4

from aioauth_fastapi.admin.storage import Storage
from .models import ClientCreate, ClientUpdate
from ..containers import ApplicationContainer
from ..oauth2.models import Client

routers = APIRouter()


@routers.post("/", response_model=Client)
@inject
async def client_create(
    request: Request,
    body: ClientCreate,
    storage: Storage = Depends(Provide[ApplicationContainer.admin_package.storage]),
) -> Client:
    client = Client(**body.dict(), user_id=request.user.id)
    await storage.create_client(client)
    return client


@routers.get("/{id}/", response_model=Client)
@inject
async def client_details(
    request: Request,
    id: UUID4,
    storage: Storage = Depends(Provide[ApplicationContainer.admin_package.storage]),
) -> Client:
    client = await storage.client_details(id, request.user.id)

    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return client


@routers.get("/", response_model=List[Client])
@inject
async def client_list(
    request: Request,
    storage: Storage = Depends(Provide[ApplicationContainer.admin_package.storage]),
) -> Optional[List[Client]]:
    return await storage.client_list(request.user.id)


@routers.delete("/{id}/")
@inject
async def client_delete(
    request: Request,
    id: UUID4,
    storage: Storage = Depends(Provide[ApplicationContainer.admin_package.storage]),
):
    await storage.client_delete(id, user_id=request.user.id)


@routers.patch("/{id}/", response_model=Client)
@inject
async def client_update(
    request: Request,
    body: ClientUpdate,
    id: UUID4,
    storage: Storage = Depends(Provide[ApplicationContainer.admin_package.storage]),
) -> Client:
    client = Client(**body.dict(exclude_unset=True), user_id=request.user.id)
    return await storage.client_update(id, client, user_id=request.user.id)
