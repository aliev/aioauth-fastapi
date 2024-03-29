from aioauth.config import Settings
from aioauth.requests import Query, Request as OAuth2Request
from aioauth.server import AuthorizationServer
from fastapi import APIRouter, Depends, Request

from aioauth_fastapi.forms import TokenForm, TokenIntrospectForm
from aioauth_fastapi.utils import to_fastapi_response, to_oauth2_request

from ..config import settings as local_settings
from ..storage.sqlalchemy import SQLAlchemyStorage, get_sqlalchemy_storage
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
    storage: SQLAlchemyStorage = Depends(get_sqlalchemy_storage),
):
    oauth2_storage = Storage(storage=storage)
    authorization_server = AuthorizationServer(storage=oauth2_storage)
    oauth2_request: OAuth2Request = await to_oauth2_request(request, settings)
    oauth2_response = await authorization_server.create_token_response(oauth2_request)
    return await to_fastapi_response(oauth2_response)


@router.post("/token/introspect")
async def token_introspect(
    request: Request,
    form: TokenIntrospectForm = Depends(),
    storage: SQLAlchemyStorage = Depends(get_sqlalchemy_storage),
):
    oauth2_storage = Storage(storage=storage)
    authorization_server = AuthorizationServer(storage=oauth2_storage)
    oauth2_request: OAuth2Request = await to_oauth2_request(request, settings)
    oauth2_response = await authorization_server.create_token_introspection_response(
        oauth2_request
    )
    return await to_fastapi_response(oauth2_response)


@router.get("/authorize")
async def authorize(
    request: Request,
    query: Query = Depends(),
    storage: SQLAlchemyStorage = Depends(get_sqlalchemy_storage),
):
    oauth2_storage = Storage(storage=storage)
    authorization_server = AuthorizationServer(storage=oauth2_storage)
    oauth2_request: OAuth2Request = await to_oauth2_request(request, settings)
    oauth2_response = await authorization_server.create_authorization_response(
        oauth2_request
    )
    return await to_fastapi_response(oauth2_response)
