from typing import TYPE_CHECKING
from http import HTTPStatus
import pytest


if TYPE_CHECKING:
    from async_asgi_testclient import TestClient
    from fastapi import FastAPI


@pytest.mark.asyncio
async def test_registration(client: "TestClient", app: "FastAPI"):
    url = app.url_path_for("users:registration")
    response = await client.post(url, json={"username": "asd", "password": "asd"})
    assert response.status_code == HTTPStatus.NO_CONTENT

    url = app.url_path_for("users:login")
    response = await client.post(url, json={"username": "asd", "password": "asd"})

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
