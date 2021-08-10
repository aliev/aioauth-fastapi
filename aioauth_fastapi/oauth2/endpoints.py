from fastapi import APIRouter, Request

from fastapi.params import Depends
from dependency_injector.wiring import inject, Provide
from ..containers import ApplicationContainer
from .utils import to_oauth2_request, to_fastapi_response
from .services import OAuth2Service

router = APIRouter()


@router.post("/token")
@inject
async def token(
    request: Request,
    oauth2_service: OAuth2Service = Depends(
        Provide[ApplicationContainer.oauth2_package.oauth2_service]
    ),
):
    oauth2_request = await to_oauth2_request(request)
    oauth2_response = await oauth2_service.token(oauth2_request)

    return await to_fastapi_response(oauth2_response)


@router.post("/token/introspect")
@inject
async def token_introspect(
    request: Request,
    oauth2_service: OAuth2Service = Depends(
        Provide[ApplicationContainer.oauth2_package.oauth2_service]
    ),
):
    oauth2_request = await to_oauth2_request(request)
    oauth2_response = await oauth2_service.token_instospection(oauth2_request)

    return await to_fastapi_response(oauth2_response)


@router.get("/authorization")
@inject
async def authorization(
    request: Request,
    oauth2_service: OAuth2Service = Depends(
        Provide[ApplicationContainer.oauth2_package.oauth2_service]
    ),
):
    oauth2_request = await to_oauth2_request(request)
    oauth2_response = await oauth2_service.authorization(oauth2_request)

    return await to_fastapi_response(oauth2_response)
