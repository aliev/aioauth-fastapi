from aioauth_fastapi.users.containers import UserContainer
from aioauth_fastapi.oauth2.containers import OAuth2Container
from dependency_injector import containers, providers
from .config import settings
from .storage.db import Database
from .storage.redis import init_redis_pool


class ApplicationContainer(containers.DeclarativeContainer):
    redis = providers.Resource(init_redis_pool)
    database = providers.Singleton(Database, settings.PSQL_DSN)

    user_package = providers.Container(
        UserContainer,
        database=database,
        redis=redis,
    )

    oauth2_package = providers.Container(
        OAuth2Container,
        database=database,
    )
