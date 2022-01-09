from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import UUID4

from ..oauth2.models import Client
from ..storage.sqlalchemy import SQLAlchemyStorage, get_sqlalchemy_storage
from .crud import SQLAlchemyCRUD
from .models import ClientCreate, ClientUpdate

routers = APIRouter()


@routers.post("/", response_model=Client)
async def client_create(
    request: Request,
    body: ClientCreate,
    storage: SQLAlchemyStorage = Depends(get_sqlalchemy_storage),
) -> Client:
    crud = SQLAlchemyCRUD(storage=storage)
    return await crud.create(**{**body.dict(), "user_id": request.user.id})


@routers.get("/{id}/", response_model=Client)
async def client_details(
    request: Request,
    id: UUID4,
    storage: SQLAlchemyStorage = Depends(get_sqlalchemy_storage),
) -> Client:
    crud = SQLAlchemyCRUD(storage=storage)
    client = await crud.details(id, request.user.id)

    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return client


@routers.get("/", response_model=List[Client])
async def client_list(
    request: Request, storage: SQLAlchemyStorage = Depends(get_sqlalchemy_storage)
) -> Optional[List[Client]]:
    crud = SQLAlchemyCRUD(storage=storage)
    return await crud.list(request.user.id)


@routers.delete("/{id}/")
async def client_delete(
    request: Request,
    id: UUID4,
    storage: SQLAlchemyStorage = Depends(get_sqlalchemy_storage),
):
    crud = SQLAlchemyCRUD(storage=storage)
    await crud.delete(id, user_id=request.user.id)


@routers.patch("/{id}/", response_model=Client)
async def client_update(
    request: Request,
    body: ClientUpdate,
    id: UUID4,
    storage: SQLAlchemyStorage = Depends(get_sqlalchemy_storage),
) -> Client:
    crud = SQLAlchemyCRUD(storage=storage)
    return await crud.update(
        id, **{**body.dict(exclude_unset=True), "user_id": request.user.id}
    )
