from http import HTTPStatus

import pytest
from async_asgi_testclient import TestClient

from aioauth_fastapi_demo.app import app


@pytest.mark.asyncio
async def test_registration(http_client: TestClient):
    # Registration
    url = app.url_path_for("users:registration")
    response = await http_client.post(url, json={"username": "asd", "password": "asd"})
    assert response.status_code == HTTPStatus.NO_CONTENT

    # Login
    url = app.url_path_for("users:login")
    response = await http_client.post(url, json={"username": "asd", "password": "asd"})

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies
