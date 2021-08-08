from aioauth_fastapi.users.repositories import UserRepository
from http import HTTPStatus

from fastapi import HTTPException, Response

from .exceptions import DuplicateUserException
from .responses import TokenResponse
from .requests import UserLoginRequest, UserRegistrationRequest

from ..crypto import encode_jwt
from ..config import settings


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.repository = user_repository

    def _generate_tokens_pair(self, user_id: str):
        general_options = {"identity": user_id, "secret": settings.JWT_PRIVATE_KEY}

        access_token = encode_jwt(
            **general_options,
            expires_delta=settings.ACCESS_TOKEN_EXP,
            token_type="access",
        )

        refresh_token = encode_jwt(
            **general_options,
            expires_delta=settings.REFRESH_TOKEN_EXP,
            token_type="refresh",
        )

        return access_token, refresh_token

    async def user_login(self, body: UserLoginRequest):

        user = await self.repository.get_user(username=body.username)

        if user is None:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

        is_verified = user.verify_password(body.password)

        if is_verified:
            access_token, refresh_token = self._generate_tokens_pair(str(user.id))
            # decoded_refresh_token = decode_jwt(refresh_token, settings.JWT_PUBLIC_KEY)

            return TokenResponse(access_token=access_token, refresh_token=refresh_token)

        return HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    async def user_registration(self, body: UserRegistrationRequest) -> Response:
        try:
            await self.repository.create_user(**body.dict())
        except DuplicateUserException:
            raise HTTPException(
                detail="User with this username already exists",
                status_code=HTTPStatus.BAD_REQUEST,
            )

        return Response(status_code=HTTPStatus.NO_CONTENT)
