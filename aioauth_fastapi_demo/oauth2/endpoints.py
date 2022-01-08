from fastapi import Request, Depends, APIRouter
from aioauth.config import Settings

from aioauth.server import AuthorizationServer
from aioauth_fastapi_demo.storage.sqlalchemy import (
    SQLAlchemyStorage,
    get_sqlalchemy_storage,
)

from aioauth_fastapi.forms import TokenForm, TokenIntrospectForm
from aioauth_fastapi.utils import to_fastapi_response, to_oauth2_request
from aioauth.requests import Query

from ..config import settings as local_settings
from .storage import Storage

router = APIRouter()

settings = Settings(
    TOKEN_EXPIRES_IN=local_settings.ACCESS_TOKEN_EXP,
    REFRESH_TOKEN_EXPIRES_IN=local_settings.REFRESH_TOKEN_EXP,
    INSECURE_TRANSPORT=local_settings.DEBUG,
)


@router.post("/token")
async def token(
    request: Request,
    form: TokenForm = Depends(),
    database: SQLAlchemyStorage = Depends(get_sqlalchemy_storage),
):
    storage = Storage(database=database)
    authorization_server = AuthorizationServer(storage=storage)
    oauth2_request = await to_oauth2_request(request, settings)
    oauth2_response = await authorization_server.create_token_response(oauth2_request)
    return await to_fastapi_response(oauth2_response)


@router.post("/token/introspect")
async def token_introspect(
    request: Request,
    form: TokenIntrospectForm = Depends(),
    database: SQLAlchemyStorage = Depends(get_sqlalchemy_storage),
):
    storage = Storage(database=database)
    authorization_server = AuthorizationServer(storage=storage)
    oauth2_request = await to_oauth2_request(request, settings)
    oauth2_response = await authorization_server.create_token_introspection_response(
        oauth2_request
    )
    return await to_fastapi_response(oauth2_response)


@router.get("/authorize")
async def authorize(
    request: Request,
    query: Query = Depends(),
    database: SQLAlchemyStorage = Depends(get_sqlalchemy_storage),
):
    storage = Storage(database=database)
    authorization_server = AuthorizationServer(storage=storage)
    oauth2_request = await to_oauth2_request(request, settings)
    oauth2_response = await authorization_server.create_authorization_response(
        oauth2_request
    )
    return await to_fastapi_response(oauth2_response)
