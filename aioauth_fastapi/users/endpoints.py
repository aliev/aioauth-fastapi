from fastapi import Response
from aioauth_fastapi.users.services import UserService
from fastapi.params import Depends
from fastapi import APIRouter

from .requests import UserLoginRequest, UserRegistrationRequest
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
    response: Response,
    body: UserLoginRequest,
    user_service: UserService = Depends(
        Provide[ApplicationContainer.user_package.user_service]
    ),
):
    return await user_service.user_login(body, response)
