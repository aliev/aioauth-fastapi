from http import HTTPStatus
from urllib import parse

import pytest
from aioauth.types import GrantType, ResponseType, TokenType
from async_asgi_testclient import TestClient

from aioauth_fastapi_demo.oauth2.models import Client
from aioauth_fastapi_demo.users.crypto import get_jwt
from aioauth_fastapi_demo.users.models import User


@pytest.mark.asyncio
async def test_authorization_code_flow(
    http_client: TestClient, user: "User", client: "Client"
):
    access_token, _ = get_jwt(user)

    response = await http_client.get(
        "/oauth2/authorize",
        query_string={
            "response_type": f"{ResponseType.TYPE_CODE.value} {ResponseType.TYPE_ID_TOKEN.value}",
            "client_id": client.client_id,
            "redirect_uri": client.redirect_uris[0],
            "scope": "openid email profile",
            "nonce": "73Ncd3",
        },
        headers={"Authorization": f"Bearer {access_token}"},
        allow_redirects=False,
    )

    assert response.status_code == HTTPStatus.FOUND

    parsed_location = parse.urlparse(response.headers.get("location"))
    parsed_qs = parse.parse_qs(parsed_location.query)

    assert "code" in parsed_qs.keys()
    assert "scope" in parsed_qs.keys()
    assert "id_token" in parsed_qs.keys()

    response = await http_client.post(
        "/oauth2/token",
        form={
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
        form={
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
        form={
            "grant_type": GrantType.TYPE_REFRESH_TOKEN.value,
            "refresh_token": refresh_token,
            "client_id": client.client_id,
            "client_secret": client.client_secret,
        },
    )
    assert (
        response.status_code == HTTPStatus.BAD_REQUEST
    ), "re-trying to revoke an already revoked token should be rejected"


@pytest.mark.asyncio
async def test_implicit_flow(http_client: TestClient, user: "User", client: "Client"):
    access_token, _ = get_jwt(user)

    response = await http_client.get(
        "/oauth2/authorize",
        query_string={
            "response_type": ResponseType.TYPE_TOKEN.value,
            "client_id": client.client_id,
            "redirect_uri": client.redirect_uris[0],
        },
        headers={"Authorization": f"Bearer {access_token}"},
        allow_redirects=False,
    )

    assert response.headers.get("location")


@pytest.mark.asyncio
async def test_token_introspection(
    http_client: TestClient, user: "User", client: "Client"
):
    access_token, _ = get_jwt(user)

    with pytest.raises(TypeError):
        introspect_response = await http_client.post(
            "/oauth2/token/introspect",
            form={"token": access_token, "token_type": TokenType.ACCESS.value},
            # empty basic auth header to ensure get client passes
            headers={"Authorization": "Basic Og=="},
        )

    # correct case
    introspect_response = await http_client.post(
        "/oauth2/token/introspect",
        form={"token": access_token, "token_type_hint": TokenType.ACCESS.value},
        headers={"Authorization": "Basic Og=="},
    )

    assert introspect_response.status_code == HTTPStatus.OK
