import pytest
import httpx
import uuid
from http import HTTPStatus
from aioauth.types import GrantType, ResponseType
from sqlalchemy.sql.expression import select
from aioauth_fastapi_demo.oauth2.models import Client
from aioauth_fastapi_demo.users.crypto import get_jwt
from httpx import AsyncClient
from aioauth_fastapi_demo.users.models import User
from aioauth_fastapi_demo.storage.sqlalchemy import SQLAlchemy


@pytest.mark.asyncio
async def test_create_oauth2_client(
    http_client: AsyncClient,
    user: User,
    db: SQLAlchemy,
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
        "/api/admin/",
        cookies=cookies,
        follow_redirects=False,
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
