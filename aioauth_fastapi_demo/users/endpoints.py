from http import HTTPStatus
from fastapi import HTTPException, Response, APIRouter
from fastapi.params import Depends
from aioauth_fastapi_demo.storage.init import get_database

from aioauth_fastapi_demo.storage.sqlalchemy import SQLAlchemy
from .storage import Storage
from .requests import UserLogin, UserRegistration
from .crypto import get_jwt
from .responses import TokenResponse
from ..config import settings

router = APIRouter()


@router.post("/registration", name="users:registration")
async def user_registration(
    body: UserRegistration,
    database: SQLAlchemy = Depends(get_database)
):
    storage = Storage(database=database)
    await storage.create_user(**body.dict())
    return Response(status_code=HTTPStatus.NO_CONTENT)


@router.post("/login", name="users:login")
async def user_login(
    response: Response,
    body: UserLogin,
    database: SQLAlchemy = Depends(get_database)
):
    storage = Storage(database=database)
    user = await storage.get_user(username=body.username)

    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    is_verified = user.verify_password(body.password)

    if is_verified:
        access_token, refresh_token = get_jwt(user)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            expires=settings.ACCESS_TOKEN_EXP,
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            expires=settings.REFRESH_TOKEN_EXP,
        )

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
