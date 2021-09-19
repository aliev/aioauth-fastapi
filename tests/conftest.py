from typing import TYPE_CHECKING
from async_asgi_testclient import TestClient
import pytest
from alembic.config import main
from Crypto.PublicKey import RSA

rsa = RSA.generate(2048)


if TYPE_CHECKING:
    from fastapi.applications import FastAPI


@pytest.fixture(autouse=True)
def settings(monkeypatch):
    monkeypatch.setenv("JWT_PUBLIC_KEY", rsa.public_key().export_key().decode())
    monkeypatch.setenv("JWT_PRIVATE_KEY", rsa.export_key().decode())
    monkeypatch.setenv(
        "PSQL_DSN", "postgresql+asyncpg://ali@localhost/aioauth_fastapi_test"
    )


@pytest.fixture(autouse=True)
def migrations(settings):
    # Run migrations
    main(["--raiseerr", "upgrade", "head"])
    yield
    # Downgrade
    main(["--raiseerr", "downgrade", "base"])


@pytest.fixture
def app() -> "FastAPI":
    from aioauth_fastapi.app import app as _app

    return _app


@pytest.fixture
@pytest.mark.asyncio
async def client(app: "FastAPI"):
    async with TestClient(app) as client:
        yield client
