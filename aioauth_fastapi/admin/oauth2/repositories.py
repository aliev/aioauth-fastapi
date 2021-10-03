from pydantic.types import UUID4
from sqlalchemy.sql.expression import select
from aioauth_fastapi.oauth2.models import Client
from aioauth_fastapi.storage.db import Database
from aioauth_fastapi.storage.exceptions import ObjectDoesNotExist


class Oauth2AdminRepository:
    def __init__(self, database: Database) -> None:
        self.database = database

    async def create_client(self, client: Client) -> None:
        await self.database.add(client)

    async def client_delete(self, id: UUID4, user_id: UUID4) -> None:
        q_results = await self.database.select(
            select(Client).where(Client.id == id).where(Client.user_id == user_id)
        )

        client = q_results.one_or_none()

        if not client:
            raise ObjectDoesNotExist

        await self.database.delete(client)
