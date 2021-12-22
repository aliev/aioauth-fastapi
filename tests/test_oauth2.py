from aioauth_fastapi_demo.users.crypto import get_jwt
from http import HTTPStatus
import pytest
from urllib import parse
from aioauth.types import GrantType, ResponseType
from aioauth_fastapi_demo.users.models import User
from aioauth_fastapi_demo.oauth2.models import Client
from typing import TYPE_CHECKING
import httpx


if TYPE_CHECKING:  # pragma: no cover
    from httpx import AsyncClient


@pytest.mark.asyncio
async def test_authorization_code_flow(
    http_client: "AsyncClient", user: "User", client: "Client"
):
    access_token, _ = get_jwt(user)

    cookies = httpx.Cookies()
    cookies.set("access_token", access_token)

    params = httpx.QueryParams()
    params = params.set(
        "response_type",
        f"{ResponseType.TYPE_CODE.value} {ResponseType.TYPE_ID_TOKEN.value}",
    )
    params = params.set("client_id", client.client_id)
    params = params.set("redirect_uri", client.redirect_uris[0])
    params = params.set("scope", "openid email profile")
    params = params.set("nonce", "73Ncd3")

    response = await http_client.get(
        "/oauth2/authorize", params=params, cookies=cookies, allow_redirects=False
    )

    assert response.status_code == HTTPStatus.FOUND

    parsed_location = parse.urlparse(response.headers.get("location"))
    parsed_qs = parse.parse_qs(parsed_location.query)

    assert "code" in parsed_qs.keys()
    assert "scope" in parsed_qs.keys()
    assert "id_token" in parsed_qs.keys()

    response = await http_client.post(
        "/oauth2/token",
        data={
            "grant_type": GrantType.TYPE_AUTHORIZATION_CODE.value,
            "redirect_uri": client.redirect_uris[0],
            "client_id": client.client_id,
            "client_secret": client.client_secret,
            "code": parsed_qs["code"][0],
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

    # re-try token revokation with revoked token should be rejected
    response = await http_client.post(
        "/oauth2/token",
        data={
            "grant_type": GrantType.TYPE_REFRESH_TOKEN.value,
            "refresh_token": refresh_token,
            "client_id": client.client_id,
            "client_secret": client.client_secret,
        },
    )
    assert (
        response.status_code == HTTPStatus.BAD_REQUEST
    ), "re-try token revokation with revoked token should be rejected"


@pytest.mark.asyncio
async def test_implicit_flow(
    http_client: "AsyncClient", user: "User", client: "Client"
):
    access_token, _ = get_jwt(user)

    cookies = httpx.Cookies()
    cookies.set("access_token", access_token)

    params = httpx.QueryParams()
    params = params.set("response_type", ResponseType.TYPE_TOKEN.value)
    params = params.set("client_id", client.client_id)
    params = params.set("redirect_uri", client.redirect_uris[0])

    response = await http_client.get(
        "/oauth2/authorize", params=params, cookies=cookies, allow_redirects=False
    )

    assert response.headers.get("location")
