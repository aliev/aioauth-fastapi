from dependency_injector import containers, providers

from .config import settings
from .oauth2.containers import OAuth2Container
from .storage.sqlalchemy import SQLAlchemy
from .users.containers import UserContainer
from .admin.containers import AdminContainer


class ApplicationContainer(containers.DeclarativeContainer):
    database = providers.Singleton(SQLAlchemy, settings.PSQL_DSN)

    user_package = providers.Container(
        UserContainer,
        database=database,
    )
    admin_package = providers.Container(AdminContainer, database=database)
    oauth2_package = providers.Container(OAuth2Container, database=database)
