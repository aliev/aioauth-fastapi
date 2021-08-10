from typing import Optional
from aioauth_fastapi.storage.db import Database
from aioauth.requests import Request
from aioauth.models import Token, AuthorizationCode, Client
from aioauth.storage import BaseStorage


class OAuth2Repository(BaseStorage):
    def __init__(self, database: Database):
        self.database = database

    async def create_token(self, request: Request, client_id: str, scope: str) -> Token:
        return await super().create_token(request, client_id, scope)

    async def save_token(self, token: Token) -> None:
        return await super().save_token(token)

    async def get_token(
        self,
        request: Request,
        client_id: str,
        access_token: Optional[str],
        refresh_token: Optional[str],
    ) -> Optional[Token]:
        return await super().get_token(
            request, client_id, access_token=access_token, refresh_token=refresh_token
        )

    async def create_authorization_code(
        self,
        request: Request,
        client_id: str,
        scope: str,
        response_type: str,
        redirect_uri: str,
        code_challenge_method: Optional[str],
        code_challenge: Optional[str],
    ) -> AuthorizationCode:
        return await super().create_authorization_code(
            request,
            client_id,
            scope,
            response_type,
            redirect_uri,
            code_challenge_method,
            code_challenge,
        )

    async def get_id_token(
        self,
        request: Request,
        client_id: str,
        scope: str,
        response_type: str,
        redirect_uri: str,
        nonce: str,
    ) -> str:
        return await super().get_id_token(
            request, client_id, scope, response_type, redirect_uri, nonce
        )

    async def save_authorization_code(
        self, authorization_code: AuthorizationCode
    ) -> None:
        return await super().save_authorization_code(authorization_code)

    async def get_client(
        self, request: Request, client_id: str, client_secret: Optional[str]
    ) -> Optional[Client]:
        return await super().get_client(request, client_id, client_secret=client_secret)

    async def authenticate(self, request: Request) -> bool:
        return await super().authenticate(request)

    async def get_authorization_code(
        self, request: Request, client_id: str, code: str
    ) -> Optional[AuthorizationCode]:
        return await super().get_authorization_code(request, client_id, code)

    async def delete_authorization_code(
        self, request: Request, client_id: str, code: str
    ) -> None:
        return await super().delete_authorization_code(request, client_id, code)

    async def revoke_token(self, request: Request, refresh_token: str) -> None:
        return await super().revoke_token(request, refresh_token)
