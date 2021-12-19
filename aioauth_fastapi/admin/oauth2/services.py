from fastapi import Request, HTTPException, status
from pydantic.types import UUID4

from aioauth_fastapi.oauth2.models import Client
from .models import ClientCreate, ClientUpdate
from typing import TYPE_CHECKING, List, Optional


if TYPE_CHECKING:
    from .repositories import Oauth2AdminRepository


class BaseService:
    def __init__(self, oauth2_admin_repository: "Oauth2AdminRepository") -> None:
        self.repository = oauth2_admin_repository


class Oauth2ClientService(BaseService):
    async def client_create(self, *, request: Request, body: ClientCreate) -> Client:
        client = Client(**body.dict(), user_id=request.user.id)

        await self.repository.create_client(client)

        return client

    async def client_list(self, *, request: Request) -> Optional[List[Client]]:

        return await self.repository.client_list(request.user.id)

    async def client_details(self, *, request: Request, id: UUID4) -> Client:

        client = await self.repository.client_details(id, request.user.id)

        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return client

    async def client_delete(self, *, request: Request, id: UUID4) -> None:
        await self.repository.client_delete(id, user_id=request.user.id)

    async def client_update(
        self, *, request: Request, body: ClientUpdate, id: UUID4
    ) -> Client:
        client = Client(**body.dict(exclude_unset=True), user_id=request.user.id)
        return await self.repository.client_update(id, client, user_id=request.user.id)


class Oauth2AdminService(Oauth2ClientService):
    ...
