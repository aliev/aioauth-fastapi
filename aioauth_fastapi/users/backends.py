import jwt
from jwt.exceptions import PyJWTError, DecodeError
from ..config import settings
from .models import AnonymousUser, User
from starlette.authentication import AuthCredentials, AuthenticationBackend


class JWTAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        token: str = request.cookies.get("token")

        if not token:
            return AuthCredentials(), AnonymousUser()

        key = settings.JWT_PUBLIC_KEY

        try:
            token_header = jwt.get_unverified_header(token)
            decoded_token = jwt.decode(token, key, algorithms=token_header.get("alg"))
        except (PyJWTError, DecodeError):
            return AuthCredentials(), AnonymousUser()
        else:
            return AuthCredentials(), User(id=decoded_token.get("sub"), **decoded_token)
