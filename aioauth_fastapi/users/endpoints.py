from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Response
from fastapi.params import Depends

from aioauth_fastapi.users.services import UserService

from ..containers import ApplicationContainer
from .requests import UserLoginRequest, UserRegistrationRequest

router = APIRouter()


@router.post("/registration", name="users:registration")
@inject
async def user_registration(
    body: UserRegistrationRequest,
    user_service: UserService = Depends(
        Provide[ApplicationContainer.user_package.user_service]
    ),
):
    return await user_service.user_registration(body)


@router.post("/login", name="users:login")
@inject
async def user_login(
    response: Response,
    body: UserLoginRequest,
    user_service: UserService = Depends(
        Provide[ApplicationContainer.user_package.user_service]
    ),
):
    return await user_service.user_login(body, response)
