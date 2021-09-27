from aioauth_fastapi.users.crypto import get_jwt
from uuid import uuid4
from http import HTTPStatus
import pytest
from aioauth.types import GrantType, ResponseType
from aioauth_fastapi.users.models import User
from aioauth_fastapi.oauth2.models import Client
from typing import TYPE_CHECKING
from urllib.parse import urlparse, parse_qs
import httpx


if TYPE_CHECKING:  # pragma: no cover
    from httpx import AsyncClient
    from aioauth_fastapi.storage.db import Database


@pytest.mark.asyncio
async def test_authorization_code_flow(db: "Database", client: "AsyncClient"):
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

    access_token, _ = get_jwt(user)

    cookies = httpx.Cookies()
    cookies.set("token", access_token)

    params = httpx.QueryParams()
    params = params.set("response_type", ResponseType.TYPE_CODE.value)
    params = params.set("client_id", client_id)
    params = params.set("redirect_uri", redirect_uris[0])

    response = await client.get(
        "/oauth2/authorize", params=params, cookies=cookies, allow_redirects=False
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.headers.get("location")

    # response = await client.get(
    #     "/oauth2/authorize", params=params, allow_redirects=False
    # )

    # response.status_code == HTTPStatus.UNAUTHORIZED

    parsed_uri = urlparse(response.headers.get("location"))
    parsed_qs = parse_qs(parsed_uri.query)

    response = await client.post(
        "/oauth2/token",
        data={
            "grant_type": GrantType.TYPE_AUTHORIZATION_CODE.value,
            "redirect_uri": redirect_uris[0],
            "client_id": client_id,
            "client_secret": client_secret,
            "code": parsed_qs.get("code")[0],
        },
    )

    assert "access_token" in response.json()
