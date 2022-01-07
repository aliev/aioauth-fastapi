from aioauth_fastapi_demo.users.crypto import authenticate
from starlette.authentication import AuthCredentials, AuthenticationBackend
from fastapi.security.utils import get_authorization_scheme_param

from ..config import settings
from .models import User, UserAnonymous


class TokenAuthenticationBackend(AuthenticationBackend):
    async def authenticate(self, request):
        authorization: str = request.headers.get("Authorization")
        _, bearer_token = get_authorization_scheme_param(authorization)

        if not bearer_token:
            return AuthCredentials(), UserAnonymous()

        key = settings.JWT_PUBLIC_KEY

        is_authenticated, decoded_token = authenticate(token=bearer_token, key=key)

        if is_authenticated:
            return AuthCredentials(), User(
                id=decoded_token["sub"],
                is_superuser=decoded_token["is_superuser"],
                is_blocked=decoded_token["is_blocked"],
                is_active=decoded_token["is_active"],
                username=decoded_token["username"],
            )

        return AuthCredentials(), UserAnonymous()
