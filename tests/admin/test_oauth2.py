import uuid
from http import HTTPStatus

import pytest
from async_asgi_testclient import TestClient
from sqlalchemy.sql.expression import select

from aioauth_fastapi_demo.oauth2.models import Client
from aioauth_fastapi_demo.storage.sqlalchemy import SQLAlchemyStorage
from aioauth_fastapi_demo.users.crypto import get_jwt
from aioauth_fastapi_demo.users.models import User


@pytest.mark.asyncio
async def test_create_oauth2_client(
    http_client: TestClient,
    user: User,
    db: SQLAlchemyStorage,
):
    access_token, _ = get_jwt(user)

    client_id = str(uuid.uuid4())
    client_secret = str(uuid.uuid4())

    body = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_types": ["authorization_code"],
        "response_types": ["code"],
        "redirect_uris": ["https://ownauth.com/callback"],
        "scope": "read write",
    }

    response = await http_client.post(
        "/api/admin/",
        headers={"Authorization": f"Bearer {access_token}"},
        allow_redirects=False,
        json=body,
    )

    assert response.status_code == HTTPStatus.OK

    response_json = response.json()

    results = await db.select(select(Client).where(Client.id == response_json["id"]))

    client = results.scalars().one_or_none()

    assert client
