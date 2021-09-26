from uuid import uuid4
from http import HTTPStatus
import pytest
from aioauth.types import GrantType, ResponseType
from aioauth_fastapi.users.models import User
from aioauth_fastapi.oauth2.models import Client
from typing import TYPE_CHECKING
import httpx


if TYPE_CHECKING:
    from httpx import AsyncClient
    from aioauth_fastapi.storage.db import Database
    from fastapi.applications import FastAPI


@pytest.mark.asyncio
async def test_oauth2(db: "Database", client: "AsyncClient", app: "FastAPI"):
    user = User(is_superuser=True, is_active=True, username="admin@admin.com")
    user.set_password("123")

    async with db.session() as session:
        session.add(user)
        await session.commit()

    client_id = uuid4()
    client_secret = uuid4()
    grant_types = [
        GrantType.TYPE_AUTHORIZATION_CODE.value,
        GrantType.TYPE_CLIENT_CREDENTIALS.value,
        GrantType.TYPE_PASSWORD.value,
        GrantType.TYPE_REFRESH_TOKEN.value,
    ]
    response_types = [
        ResponseType.TYPE_ID_TOKEN.value,
        ResponseType.TYPE_CODE.value,
        ResponseType.TYPE_NONE.value,
        ResponseType.TYPE_TOKEN.value,
    ]

    redirect_uris = ["https://localhost"]

    scope = "read write"

    client_ = Client(
        client_id=str(client_id),
        client_secret=str(client_secret),
        response_types=response_types,
        grant_types=grant_types,
        redirect_uris=redirect_uris,
        scope=scope,
        user_id=user.id,
    )

    async with db.session() as session:
        session.add(client_)
        await session.commit()

    url = app.url_path_for("users:login")

    response = await client.post(
        url, json={"username": user.username, "password": "123"}
    )

    assert response.status_code == HTTPStatus.OK

    token = response.cookies.get("token")

    cookies = httpx.Cookies()
    cookies.set("token", token)

    params = httpx.QueryParams()
    params = params.set("response_type", ResponseType.TYPE_CODE.value)
    params = params.set("client_id", client_id)
    params = params.set("redirect_uri", redirect_uris[0])

    response = await client.get(
        "/oauth2/authorize", params=params, cookies=cookies, allow_redirects=False
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.headers.get("location")
