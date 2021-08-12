import httpx
from starlette.requests import Request
from aioauth_fastapi.users.decorators import check_access_token
from aioauth_fastapi.users.services import UserService
from fastapi.params import Depends
from fastapi import APIRouter

from .requests import UserLoginRequest, UserRegistrationRequest
from .queries import AuthorizationCodeQuery
from .security import api_security
from ..containers import ApplicationContainer
from dependency_injector.wiring import inject, Provide

router = APIRouter()


@router.post("/registration")
@inject
async def user_registration(
    body: UserRegistrationRequest,
    user_service: UserService = Depends(
        Provide[ApplicationContainer.user_package.user_service]
    ),
):
    return await user_service.user_registration(body)


@router.post("/login")
@inject
async def user_login(
    body: UserLoginRequest,
    user_service: UserService = Depends(
        Provide[ApplicationContainer.user_package.user_service]
    ),
):
    return await user_service.user_login(body)


@router.post("/logout", dependencies=[api_security])
@check_access_token()
@inject
async def user_logout(
    request: Request,
    user_service: UserService = Depends(
        Provide[ApplicationContainer.user_package.user_service]
    ),
):
    return await user_service.user_logout(request)


@router.post("/token/refresh", dependencies=[api_security])
@inject
async def token_refresh():
    pass


@router.get("/callback")
async def callback(query: AuthorizationCodeQuery = Depends()):
    data = {
        "grant_type": "authorization_code",
        "scope": query.scope,
        "code": query.code,
        "client_id": "be861a8a-7817-4a9e-93d3-9976bf099893",
        "client_secret": "71569cc8-89ea-48c1-adb3-10f831020840",
        "redirect_uri": "http://127.0.0.1:8001/api/users/callback",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post("http://127.0.0.1:8001/oauth2/token", data=data)
        return response.json()
