from aioauth.config import Settings
from aioauth.fastapi.router import get_oauth2_router
from aioauth.server import AuthorizationServer
from aioauth_fastapi_demo.storage.init import get_database

from ..config import settings
from .storage import Storage


def get_router():
    database = get_database()
    storage = Storage(database=database)
    authorization_server = AuthorizationServer(storage=storage)

    return get_oauth2_router(
        authorization_server,
        settings=Settings(
            TOKEN_EXPIRES_IN=settings.ACCESS_TOKEN_EXP,
            REFRESH_TOKEN_EXPIRES_IN=settings.REFRESH_TOKEN_EXP,
            INSECURE_TRANSPORT=settings.DEBUG,
        ),
    )
