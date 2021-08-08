from starlette.requests import Request
from aioauth_fastapi.users.decorators import check_access_token
from aioauth_fastapi.users.services import UserService
from fastapi.params import Depends
from fastapi import APIRouter

from .requests import UserLoginRequest, UserRegistrationRequest
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
