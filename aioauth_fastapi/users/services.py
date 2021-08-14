from starlette.requests import Request
from aioauth_fastapi.users.repositories import UserRepository
from http import HTTPStatus

from fastapi import HTTPException, Response

from .exceptions import DuplicateUserException
from .responses import TokenResponse
from .requests import UserLoginRequest, UserRegistrationRequest

from .crypto import get_jwt


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.repository = user_repository

    async def user_login(
        self, body: UserLoginRequest, response: Response
    ) -> TokenResponse:

        user = await self.repository.get_user(username=body.username)

        if user is None:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

        is_verified = user.verify_password(body.password)

        if is_verified:
            access_token, refresh_token = get_jwt(user)

            response.set_cookie(key="token", value=access_token, httponly=True)

            return TokenResponse(access_token=access_token, refresh_token=refresh_token)

        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    async def user_registration(self, body: UserRegistrationRequest) -> Response:
        try:
            await self.repository.create_user(**body.dict())
        except DuplicateUserException:
            raise HTTPException(
                detail="User with this username already exists",
                status_code=HTTPStatus.BAD_REQUEST,
            )

        return Response(status_code=HTTPStatus.NO_CONTENT)

    async def user_logout(self, request: Request) -> Response:
        """
        Remove refresh_token from whitelisted tokens.
        """
