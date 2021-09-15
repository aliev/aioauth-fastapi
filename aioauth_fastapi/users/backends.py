import jwt
from jwt.exceptions import DecodeError, PyJWTError
from starlette.authentication import AuthCredentials, AuthenticationBackend

from ..config import settings
from .models import User, UserAnonymous


class CookiesAuthenticationBackend(AuthenticationBackend):
    async def authenticate(self, request):
        token: str = request.cookies.get("token")

        if not token:
            return AuthCredentials(), UserAnonymous()

        key = settings.JWT_PUBLIC_KEY

        try:
            token_header = jwt.get_unverified_header(token)
            decoded_token = jwt.decode(token, key, algorithms=token_header.get("alg"))
        except (PyJWTError, DecodeError):
            return AuthCredentials(), UserAnonymous()
        else:
            return AuthCredentials(), User(id=decoded_token.get("sub"), **decoded_token)
