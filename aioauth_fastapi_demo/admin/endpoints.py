from typing import List, Optional
from fastapi import Request, HTTPException, status, APIRouter
from fastapi.params import Depends
from pydantic import UUID4

from aioauth_fastapi_demo.admin.storage import Storage
from aioauth_fastapi_demo.storage.init import get_database
from aioauth_fastapi_demo.storage.sqlalchemy import SQLAlchemy
from .models import ClientCreate, ClientUpdate
from ..oauth2.models import Client

routers = APIRouter()


@routers.post("/", response_model=Client)
async def client_create(
    request: Request,
    body: ClientCreate,
    database: SQLAlchemy = Depends(get_database)
) -> Client:
    storage = Storage(database=database)
    client = Client(**body.dict(), user_id=request.user.id)
    await storage.create_client(client)
    return client


@routers.get("/{id}/", response_model=Client)
async def client_details(
    request: Request,
    id: UUID4,
    database: SQLAlchemy = Depends(get_database)
) -> Client:
    storage = Storage(database=database)
    client = await storage.client_details(id, request.user.id)

    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return client


@routers.get("/", response_model=List[Client])
async def client_list(
    request: Request,
    database: SQLAlchemy = Depends(get_database)
) -> Optional[List[Client]]:
    storage = Storage(database=database)
    return await storage.client_list(request.user.id)


@routers.delete("/{id}/")
async def client_delete(
    request: Request,
    id: UUID4,
    database: SQLAlchemy = Depends(get_database)
):
    storage = Storage(database=database)
    await storage.client_delete(id, user_id=request.user.id)


@routers.patch("/{id}/", response_model=Client)
async def client_update(
    request: Request,
    body: ClientUpdate,
    id: UUID4,
    database: SQLAlchemy = Depends(get_database)
) -> Client:
    storage = Storage(database=database)
    client = Client(**body.dict(exclude_unset=True), user_id=request.user.id)
    return await storage.client_update(id, client, user_id=request.user.id)
