from typing import List, Optional

from pydantic.types import UUID4
from sqlalchemy.sql.expression import delete, select, update

from ..oauth2.models import Client
from ..storage.sqlalchemy import SQLAlchemyStorage


class CRUD:
    def __init__(self, storage: SQLAlchemyStorage) -> None:
        self.storage = storage

    async def list(self, user_id: UUID4) -> Optional[List[Client]]:
        q_results = await self.storage.select(
            select(Client).where(Client.user_id == user_id)
        )

        return q_results.scalars().fetchall()

    async def create(self, client: Client) -> None:
        await self.storage.add(client)

    async def delete(self, id: UUID4, user_id: UUID4) -> None:
        await self.storage.delete(
            delete(Client).where(Client.id == id).where(Client.user_id == user_id)
        )

    async def details(self, id: UUID4, user_id: UUID4) -> Optional[Client]:
        q_results = await self.storage.select(
            select(Client).where(Client.id == id).where(Client.user_id == user_id)
        )

        return q_results.scalars().one_or_none()

    async def update(self, id: UUID4, client: Client, user_id: UUID4) -> Client:
        await self.storage.update(
            update(Client)
            .where(Client.id == id)
            .where(Client.user_id == user_id)
            .values(**client.dict(exclude={"id": True}))
        )

        return client
