from aioauth_fastapi.users.containers import UserContainer
from dependency_injector import containers, providers
from .config import settings
from .storage.db import Database


class ApplicationContainer(containers.DeclarativeContainer):
    database = providers.Singleton(Database, settings.PSQL_DSN)

    user_package = providers.Container(
        UserContainer,
        database=database,
    )
