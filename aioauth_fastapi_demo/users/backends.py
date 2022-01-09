from fastapi.security.utils import get_authorization_scheme_param
from starlette.authentication import AuthCredentials, AuthenticationBackend

from aioauth_fastapi_demo.users.crypto import authenticate

from ..config import settings
from .models import User, UserAnonymous


class TokenAuthenticationBackend(AuthenticationBackend):
    async def authenticate(self, request):
        authorization: str = request.headers.get("Authorization")
        _, bearer_token = get_authorization_scheme_param(authorization)

        token: str = request.cookies.get("access_token") or bearer_token

        if not token:
            return AuthCredentials(), UserAnonymous()

        key = settings.JWT_PUBLIC_KEY

        is_authenticated, decoded_token = authenticate(token=token, key=key)

        if is_authenticated:
            return AuthCredentials(), User(
                id=decoded_token["sub"],
                is_superuser=decoded_token["is_superuser"],
                is_blocked=decoded_token["is_blocked"],
                is_active=decoded_token["is_active"],
                username=decoded_token["username"],
            )

        return AuthCredentials(), UserAnonymous()
