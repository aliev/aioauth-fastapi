from dependency_injector import containers, providers

from .config import settings
from .oauth2.containers import OAuth2Container
from .storage.db import Database
from .users.containers import UserContainer


class ApplicationContainer(containers.DeclarativeContainer):
    database = providers.Singleton(Database, settings.PSQL_DSN)

    user_package = providers.Container(
        UserContainer,
        database=database,
    )

    oauth2_package = providers.Container(OAuth2Container, database=database)
