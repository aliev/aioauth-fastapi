from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Response
from fastapi.params import Depends

from ..storage.sqlalchemy import SQLAlchemyStorage, get_sqlalchemy_storage
from .crud import CRUD
from .crypto import get_jwt
from .requests import UserLogin, UserRegistration
from .responses import TokenResponse

router = APIRouter()


@router.post("/registration", name="users:registration")
async def user_registration(
    body: UserRegistration,
    storage: SQLAlchemyStorage = Depends(get_sqlalchemy_storage),
):
    crud = CRUD(storage=storage)
    await crud.create(**body.dict())
    return Response(status_code=HTTPStatus.NO_CONTENT)


@router.post("/login", name="users:login")
async def user_login(
    response: Response,
    body: UserLogin,
    storage: SQLAlchemyStorage = Depends(get_sqlalchemy_storage),
):
    crud = CRUD(storage=storage)
    user = await crud.get(username=body.username)

    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    is_verified = user.verify_password(body.password)

    if is_verified:
        access_token, refresh_token = get_jwt(user)
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
