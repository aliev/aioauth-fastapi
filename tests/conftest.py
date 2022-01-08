from aioauth.types import GrantType, ResponseType
from aioauth_fastapi_demo.oauth2.models import Client
import logging
from uuid import uuid4
from aioauth_fastapi_demo.users.models import User
from aioauth_fastapi_demo.storage.sqlalchemy import SQLAlchemy
import pytest
from alembic.config import main
from Crypto.PublicKey import RSA
from aioauth_fastapi_demo.app import app
from async_asgi_testclient import TestClient

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
async def db() -> SQLAlchemy:
    from aioauth_fastapi_demo.storage.sqlalchemy import get_database

    return get_database()


@pytest.fixture
@pytest.mark.asyncio
async def http_client():
    async with TestClient(application=app) as client:
        yield client


@pytest.fixture
def user_password():
    return "123"


@pytest.fixture
async def user(db: "SQLAlchemy", user_password: str) -> User:
    user = User(is_superuser=True, is_active=True, username="admin@admin.com")
    user.set_password(user_password)
    await db.add(user)

    return user


@pytest.fixture
async def client(db: "SQLAlchemy", user: "User") -> Client:
    client_id = uuid4()
    client_secret = uuid4()
    grant_types = [
        GrantType.TYPE_AUTHORIZATION_CODE.value,
        GrantType.TYPE_CLIENT_CREDENTIALS.value,
        GrantType.TYPE_PASSWORD.value,
        GrantType.TYPE_REFRESH_TOKEN.value,
    ]
    response_types = [
        ResponseType.TYPE_ID_TOKEN.value,
        ResponseType.TYPE_CODE.value,
        ResponseType.TYPE_NONE.value,
        ResponseType.TYPE_TOKEN.value,
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
