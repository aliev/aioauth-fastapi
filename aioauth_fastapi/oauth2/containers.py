from dependency_injector import containers, providers
from aioauth.server import AuthorizationServer
from .repositories import OAuth2Repository
from .services import OAuth2Service


class OAuth2Container(containers.DeclarativeContainer):
    database = providers.Dependency()

    oauth2_repository = providers.Singleton(
        OAuth2Repository,
        database=database,
    )

    authorization_server = providers.Singleton(
        AuthorizationServer,
        storage=oauth2_repository,
    )

    oauth2_service = providers.Singleton(
        OAuth2Service,
        authorization_server=authorization_server,
    )
