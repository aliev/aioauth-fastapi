from dependency_injector.wiring import Provide, inject
from fastapi.params import Depends
from aioauth.server import AuthorizationServer
from ..containers import ApplicationContainer
from ..config import settings
from aioauth.config import Settings
from aioauth.fastapi.router import get_oauth2_router


@inject
def get_router(
    authorization_server: AuthorizationServer = Depends(
        Provide[ApplicationContainer.oauth2_package.authorization_server]
    ),
):
    return get_oauth2_router(
        authorization_server,
        settings=Settings(
            TOKEN_EXPIRES_IN=settings.ACCESS_TOKEN_EXP,
            REFRESH_TOKEN_EXPIRES_IN=settings.REFRESH_TOKEN_EXP,
            INSECURE_TRANSPORT=settings.DEBUG,
        ),
    )
