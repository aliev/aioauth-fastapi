from aioredis.client import Redis
from http import HTTPStatus

from starlette.requests import Request
from fastapi import HTTPException, Response

from .exceptions import DuplicateUserException
from .storage import UserStorage
from .responses import TokenResponse
from .requests import UserLoginRequest, UserRegistrationRequest

from ..storage.db import get_sqlalchemy_async_session
from ..crypto import decode_jwt, encode_jwt
from ..config import settings
from ..storage.redis import get_redis_pool


class UserService:
    def __init__(self, request: Request, storage: UserStorage, redis: Redis) -> None:
        self.request = request
        self.storage = storage
        self.redis = redis

    def _generate_tokens_pair(self, user_id: str):
        general_options = {"user_id": user_id, "secret": settings.JWT_PRIVATE_KEY}

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

        user = await self.storage.get_user(username=body.username)

        if user is None:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

        is_verified = user.verify_password(body.password)

        if is_verified:
            access_token, refresh_token = self._generate_tokens_pair(str(user.id))
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
            await self.storage.create_user(**body.dict())
        except DuplicateUserException:
            raise HTTPException(
                detail="User with this username already exists",
                status_code=HTTPStatus.BAD_REQUEST,
            )

        return Response(status_code=HTTPStatus.NO_CONTENT)


async def get_user_service(request: Request) -> UserService:
    async_session = get_sqlalchemy_async_session()
    redis_pool = get_redis_pool()

    async with async_session() as session:
        async with session.begin():
            storage = UserStorage(session=session)

    return UserService(request=request, storage=storage, redis=redis_pool)
