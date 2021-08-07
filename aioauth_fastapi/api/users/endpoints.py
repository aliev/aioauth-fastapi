from fastapi.params import Depends
from fastapi import APIRouter, Request

from . import requests
from .services import get_user_service, UserService

router = APIRouter()


@router.post("/registration")
async def user_registration(
    request: Request,
    body: requests.UserRegistrationRequest,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.user_registration(body)


@router.post("/login")
async def user_login(
    request: Request,
    body: requests.UserLoginRequest,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.user_login(body)
