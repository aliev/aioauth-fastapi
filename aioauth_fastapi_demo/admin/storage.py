from typing import List, Optional

from pydantic.types import UUID4
from sqlalchemy.sql.expression import delete, select, update

from ..oauth2.models import Client
from ..storage.sqlalchemy import SQLAlchemyStorage


class Storage:
    def __init__(self, database: SQLAlchemyStorage) -> None:
        self.database = database

    async def client_list(self, user_id: UUID4) -> Optional[List[Client]]:
        q_results = await self.database.select(
            select(Client).where(Client.user_id == user_id)
        )

        return q_results.scalars().fetchall()

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

        return q_results.scalars().one_or_none()

    async def client_update(self, id: UUID4, client: Client, user_id: UUID4) -> Client:
        await self.database.update(
            update(Client)
            .where(Client.id == id)
            .where(Client.user_id == user_id)
            .values(**client.dict(exclude={"id": True}))
        )

        return client
