from dependency_injector import containers, providers
from aioauth.server import AuthorizationServer
from .storage import OAuth2Storage


class OAuth2Container(containers.DeclarativeContainer):

    database = providers.Dependency()

    oauth2_storage = providers.Singleton(OAuth2Storage, database=database)
    authorization_server = providers.Singleton(
        AuthorizationServer, storage=oauth2_storage
    )
