from fastapi.params import Depends
from fastapi import APIRouter, Request

from .requests import UserLoginRequest, UserRegistrationRequest
from .services import get_user_service, UserService

router = APIRouter()


@router.post("/registration")
async def user_registration(
    request: Request,
    body: UserRegistrationRequest,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.user_registration(body)


@router.post("/login")
async def user_login(
    request: Request,
    body: UserLoginRequest,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.user_login(body)
