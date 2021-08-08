from aioauth_fastapi.users.containers import UserContainer
from dependency_injector import containers, providers
from .config import settings
from .storage.db import Storage
from .storage.redis import Redis, init_redis_pool


class ApplicationContainer(containers.DeclarativeContainer):
    redis_pool = providers.Resource(init_redis_pool)

    storage = providers.Singleton(Storage, settings.PSQL_DSN)
    redis = providers.Singleton(Redis, redis_pool)

    user_package = providers.Container(
        UserContainer,
        storage=storage,
    )
