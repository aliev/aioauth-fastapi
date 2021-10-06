from http import HTTPStatus

from fastapi import HTTPException, Response

from typing import TYPE_CHECKING

from ..config import settings

from .crypto import get_jwt
from .exceptions import DuplicateUserException
from .responses import TokenResponse

if TYPE_CHECKING:
    from .requests import UserLogin, UserRegistration
    from ..users.repositories import UserRepository


class UserService:
    def __init__(self, user_repository: "UserRepository") -> None:
        self.repository = user_repository

    async def user_login(self, body: "UserLogin", response: Response) -> TokenResponse:

        user = await self.repository.get_user(username=body.username)

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

    async def user_registration(self, body: "UserRegistration") -> Response:
        try:
            await self.repository.create_user(**body.dict())
        except DuplicateUserException:
            raise HTTPException(
                detail="User with this username already exists",
                status_code=HTTPStatus.BAD_REQUEST,
            )

        return Response(status_code=HTTPStatus.NO_CONTENT)
