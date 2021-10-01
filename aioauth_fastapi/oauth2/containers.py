from aioauth.server import AuthorizationServer
from dependency_injector import containers, providers

from .repositories import OAuth2Repository


class OAuth2Container(containers.DeclarativeContainer):

    database = providers.Dependency()

    oauth2_repository = providers.Singleton(OAuth2Repository, database=database)
    authorization_server = providers.Singleton(
        AuthorizationServer, storage=oauth2_repository
    )
