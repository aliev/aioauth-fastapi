from typing import TYPE_CHECKING
from http import HTTPStatus
import pytest


if TYPE_CHECKING:  # pragma: no cover
    from httpx import AsyncClient
    from fastapi import FastAPI


@pytest.mark.asyncio
async def test_registration(client: "AsyncClient", app: "FastAPI"):
    # Registration
    url = app.url_path_for("users:registration")
    response = await client.post(url, json={"username": "asd", "password": "asd"})
    assert response.status_code == HTTPStatus.NO_CONTENT

    # User already exists
    url = app.url_path_for("users:registration")
    response = await client.post(url, json={"username": "asd", "password": "asd"})
    assert response.status_code == HTTPStatus.BAD_REQUEST

    # Login
    url = app.url_path_for("users:login")
    response = await client.post(url, json={"username": "asd", "password": "asd"})

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert response.cookies.get("token")
