import logging
from uuid import uuid4

import pytest
from alembic.config import main
from async_asgi_testclient import TestClient
from Crypto.PublicKey import RSA

from aioauth_fastapi_demo.app import app
from aioauth_fastapi_demo.oauth2.models import Client
from aioauth_fastapi_demo.storage.sqlalchemy import SQLAlchemyStorage
from aioauth_fastapi_demo.users.models import User

rsa = RSA.generate(2048)


@pytest.fixture(autouse=True)
def settings():
    from aioauth_fastapi_demo.config import settings as _settings

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
@pytest.mark.asyncio
async def db() -> SQLAlchemyStorage:
    from aioauth_fastapi_demo.storage.sqlalchemy import get_sqlalchemy_storage

    return get_sqlalchemy_storage()


@pytest.fixture
@pytest.mark.asyncio
async def http_client():
    async with TestClient(application=app) as client:
        yield client


@pytest.fixture
def user_password():
    return "123"


@pytest.fixture
async def user(db: "SQLAlchemyStorage", user_password: str) -> User:
    user = User(is_superuser=True, is_active=True, username="admin@admin.com")
    user.set_password(user_password)
    await db.add(user)

    return user


@pytest.fixture
async def client(db: "SQLAlchemyStorage", user: "User") -> Client:
    client_id = uuid4()
    client_secret = uuid4()
    grant_types = [
        "authorization_code",
        "client_credentials",
        "password",
        "refresh_token",
    ]
    response_types = [
        "code",
        "id_token",
        "none",
        "token",
    ]

    redirect_uris = ["https://localhost"]

    scope = "read write openid email profile"

    client = Client(
        client_id=str(client_id),
        client_secret=str(client_secret),
        response_types=response_types,
        grant_types=grant_types,
        redirect_uris=redirect_uris,
        scope=scope,
        user_id=user.id,
    )

    await db.add(client)

    return client
