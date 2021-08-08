from starlette.requests import Request
from aioauth_fastapi.users.repositories import UserRepository
from http import HTTPStatus
from aioredis.client import Redis

from fastapi import HTTPException, Response

from .exceptions import DuplicateUserException
from .responses import TokenResponse
from .requests import UserLoginRequest, UserRegistrationRequest

from ..crypto import decode_jwt, encode_jwt
from ..config import settings
from ..storage.tables import UserTable


class UserService:
    def __init__(self, user_repository: UserRepository, redis: Redis) -> None:
        self.repository = user_repository
        self.redis = redis

    def _generate_tokens_pair(self, user: UserTable):
        general_options = {
            "identity": str(user.id),
            "secret": settings.JWT_PRIVATE_KEY,
            "custom_headers": {
                "is_superuser": user.is_superuser,
                "is_blocked": user.is_blocked,
                "username": user.username,
            },
        }

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
            access_token, refresh_token = self._generate_tokens_pair(user)

            decoded_refresh_token = decode_jwt(refresh_token, settings.JWT_PUBLIC_KEY)
            # Whitelist referesh_token
            await self.redis.set(
                f"{decoded_refresh_token['sub']}",
                f"{decoded_refresh_token['jti']}",
                ex=settings.REFRESH_TOKEN_EXP,
            )

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

    async def user_logout(self, request: Request):
        """
        Remove refresh_token from whitelisted tokens.
        """
