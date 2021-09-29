from aioauth_fastapi.users.crypto import get_jwt
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


@pytest.mark.asyncio
async def test_authorization_code_flow(
    http_client: "AsyncClient", user: "User", client: "Client"
):
    access_token, _ = get_jwt(user)

    cookies = httpx.Cookies()
    cookies.set("token", access_token)

    params = httpx.QueryParams()
    params = params.set("response_type", ResponseType.TYPE_CODE.value)
    params = params.set("client_id", client.client_id)
    params = params.set("redirect_uri", client.redirect_uris[0])

    response = await http_client.get(
        "/oauth2/authorize", params=params, cookies=cookies, allow_redirects=False
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.headers.get("location")

    parsed_uri = urlparse(response.headers.get("location"))
    parsed_qs = parse_qs(parsed_uri.query)

    response = await http_client.post(
        "/oauth2/token",
        data={
            "grant_type": GrantType.TYPE_AUTHORIZATION_CODE.value,
            "redirect_uri": client.redirect_uris[0],
            "client_id": client.client_id,
            "client_secret": client.client_secret,
            "code": parsed_qs.get("code")[0],
        },
    )

    assert "access_token" in response.json()

    refresh_token = response.json()["refresh_token"]

    response = await http_client.post(
        "/oauth2/token",
        data={
            "grant_type": GrantType.TYPE_REFRESH_TOKEN.value,
            "refresh_token": refresh_token,
            "client_id": client.client_id,
            "client_secret": client.client_secret,
        },
    )

    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_implicit_flow(
    http_client: "AsyncClient", user: "User", client: "Client"
):
    access_token, _ = get_jwt(user)

    cookies = httpx.Cookies()
    cookies.set("token", access_token)

    params = httpx.QueryParams()
    params = params.set("response_type", ResponseType.TYPE_TOKEN.value)
    params = params.set("client_id", client.client_id)
    params = params.set("redirect_uri", client.redirect_uris[0])

    response = await http_client.get(
        "/oauth2/authorize", params=params, cookies=cookies, allow_redirects=False
    )

    assert response.headers.get("location")
