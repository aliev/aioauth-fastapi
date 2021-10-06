from typing import List, Optional
from pydantic.types import UUID4
from sqlalchemy.sql.expression import delete, select
from aioauth_fastapi.oauth2.models import Client
from aioauth_fastapi.storage.db import Database


class Oauth2AdminRepository:
    def __init__(self, database: Database) -> None:
        self.database = database

    async def client_list(self, user_id: UUID4) -> Optional[List[Client]]:
        q_results = await self.database.select(
            select(Client).where(Client.user_id == user_id)
        )

        return q_results.fetchall()

    async def create_client(self, client: Client) -> None:
        await self.database.add(client)

    async def client_delete(self, id: UUID4, user_id: UUID4) -> None:
        await self.database.delete(
            delete(Client).where(Client.id == id).where(Client.user_id == user_id)
        )

    async def client_details(self, id: UUID4, user_id: UUID4) -> Optional[Client]:
        q_results = await self.database.select(
            select(Client).where(Client.id == id).where(Client.user_id == user_id)
        )

        return q_results.one_or_none()
