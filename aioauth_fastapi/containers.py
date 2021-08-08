from aioauth_fastapi.users.containers import UserContainer
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
