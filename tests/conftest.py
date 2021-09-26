import logging
from aioauth_fastapi.config import Settings
from aioauth_fastapi.storage.db import Database
from typing import TYPE_CHECKING
from httpx import AsyncClient
import pytest
from alembic.config import main
from Crypto.PublicKey import RSA

rsa = RSA.generate(2048)


if TYPE_CHECKING:
    from fastapi.applications import FastAPI


@pytest.fixture(autouse=True)
def settings():
    from aioauth_fastapi.config import settings as _settings

    return _settings


@pytest.fixture(autouse=True)
def migrations():
    logger = logging.getLogger("alembic.runtime.migration")
    logger.disabled = True

    logger = logging.getLogger("sqlalchemy.engine.Engine")
    logger.disabled = True

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
def db(settings: Settings) -> Database:
    return Database(settings.PSQL_DSN)


@pytest.fixture
@pytest.mark.asyncio
async def client(app: "FastAPI"):
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
