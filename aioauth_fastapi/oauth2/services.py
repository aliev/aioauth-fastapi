from aioauth.requests import Request
from aioauth.responses import Response

from aioauth.server import AuthorizationServer


class OAuth2Service:
    def __init__(self, authorization_server: AuthorizationServer) -> None:
        self.authorization_server = authorization_server

    async def token(self, request: Request) -> Response:
        return await self.authorization_server.create_token_response(request)

    async def authorization(self, request: Request) -> Response:
        return await self.authorization_server.create_authorization_response(request)

    async def token_instospection(self, request: Request) -> Response:
        return await self.authorization_server.create_token_introspection_response(
            request
        )
