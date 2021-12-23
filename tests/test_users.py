from http import HTTPStatus
import pytest
from httpx import AsyncClient
from fastapi import FastAPI


@pytest.mark.asyncio
async def test_registration(http_client: AsyncClient, app: FastAPI):
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
    assert response.cookies.get("access_token")
