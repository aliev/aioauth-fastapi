import pytest
import httpx
import uuid
from http import HTTPStatus
from typing import TYPE_CHECKING
from aioauth.types import GrantType, ResponseType
from sqlalchemy.sql.expression import select
from aioauth_fastapi.oauth2.models import Client
from aioauth_fastapi.users.crypto import get_jwt


if TYPE_CHECKING:  # pragma: no cover
    from httpx import AsyncClient
    from aioauth_fastapi.users.models import User
    from aioauth_fastapi.storage.db import Database


@pytest.mark.asyncio
async def test_create_oauth2_client(
    http_client: "AsyncClient",
    user: "User",
    db: "Database",
):
    access_token, _ = get_jwt(user)
    cookies = httpx.Cookies()
    cookies.set("access_token", access_token)

    client_id = str(uuid.uuid4())
    client_secret = str(uuid.uuid4())

    body = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_types": [GrantType.TYPE_AUTHORIZATION_CODE],
        "response_types": [ResponseType.TYPE_CODE],
        "redirect_uris": ["https://ownauth.com/callback"],
        "scope": "read write",
    }

    response = await http_client.post(
        "/api/admin/oauth2/",
        cookies=cookies,
        allow_redirects=False,
        json=body,
    )

    assert response.status_code == HTTPStatus.OK

    response_json = response.json()

    async with db.session() as session:
        results = await session.execute(
            select(Client).where(Client.id == response_json["id"])
        )

    client = results.scalar()

    assert client
