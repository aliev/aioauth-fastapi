from typing import Optional

from aioauth.models import AuthorizationCode, Client, Token
from aioauth.requests import Request
from aioauth.storage import BaseStorage
from aioauth.types import GrantType, ResponseType, TokenType
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from aioauth_fastapi.storage.db import Database
from aioauth_fastapi.users.crypto import get_jwt

from ..users.models import User
from .models import AuthorizationCode as AuthorizationCodeDB
from .models import Client as ClientDB
from .models import Token as TokenDB


class OAuth2Storage(BaseStorage):
    def __init__(self, database: Database):
        self.database = database

    async def get_user(self, request: Request):
        user: Optional[User] = None

        if request.query.response_type == ResponseType.TYPE_TOKEN:
            # If ResponseType is token get the user from current session
            user = request.user

        if request.post.grant_type == GrantType.TYPE_AUTHORIZATION_CODE:
            # If GrantType is authorization code get user from DB by code
            q_results = await self.database.select(
                select(AuthorizationCodeDB).where(
                    AuthorizationCodeDB.code == request.post.code
                )
            )

            authorization_code: Optional[AuthorizationCodeDB]
            authorization_code = q_results.one_or_none()

            if not authorization_code:
                return

            q_results = await self.database.select(
                select(User).where(User.id == authorization_code.user_id)
            )

            user = q_results.one_or_none()

        if request.post.grant_type == GrantType.TYPE_REFRESH_TOKEN:
            # Get user from token
            q_results = await self.database.select(
                select(TokenDB)
                .where(TokenDB.refresh_token == request.post.refresh_token)
                .where(TokenDB.revoked == False)  # noqa
                .options(selectinload(TokenDB.user))
            )

            token: Optional[TokenDB]

            token = q_results.one_or_none()

            if not token:
                return

            user = token.user

        return user

    async def create_token(self, request: Request, client_id: str, scope: str) -> Token:
        """
        Create token and store it in database.
        """
        user = await self.get_user(request)

        access_token, refresh_token = get_jwt(user)

        token = await super().create_token(request, client_id, scope)

        token_params = {
            **token._asdict(),
            # Replace aioauth access/refresh tokens to JWT
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

        token_record_params = {**token_params, "user_id": user.id}

        token_record = TokenDB(**token_record_params)

        await self.database.add(token_record)

        return Token(**token_params)

    async def revoke_token(self, request: Request, refresh_token: str) -> None:
        """
        Remove refresh_token from whitelist.
        """

    async def get_token(
        self,
        request: Request,
        client_id: str,
        access_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
        token_type: Optional[str] = "refresh_token",
    ) -> Optional[Token]:
        if token_type == TokenType.REFRESH:
            q = select(TokenDB).where(TokenDB.refresh_token == refresh_token)
        else:
            q = select(TokenDB).where(TokenDB.access_token == access_token)

        q_results = await self.database.select(
            q.where(TokenDB.revoked == False).options(  # noqa
                selectinload(TokenDB.user)
            )
        )

        token_record: Optional[TokenDB]
        token_record = q_results.one_or_none()

        if token_record:
            return Token(
                access_token=token_record.access_token,
                refresh_token=token_record.refresh_token,
                scope=token_record.scope,
                issued_at=token_record.issued_at,
                expires_in=token_record.expires_in,
                refresh_token_expires_in=token_record.refresh_token_expires_in,
                client_id=client_id,
            )

    async def create_authorization_code(
        self, request: Request, *args, **kwargs
    ) -> AuthorizationCode:
        authorization_code = await super().create_authorization_code(
            request, *args, **kwargs
        )

        authorization_code_record = AuthorizationCodeDB(
            **{
                **authorization_code._asdict(),
                "user_id": request.user.id,
            }
        )

        await self.database.add(authorization_code_record)

        return authorization_code

    async def get_client(
        self, request: Request, client_id: str, client_secret: Optional[str] = None
    ) -> Optional[Client]:
        q_results = await self.database.select(
            select(ClientDB).where(ClientDB.client_id == client_id)
        )

        client_record: Optional[ClientDB]
        client_record = q_results.one_or_none()

        if client_record:
            return Client(
                client_id=client_record.client_id,
                client_secret=client_record.client_secret,
                grant_types=client_record.grant_types,
                response_types=client_record.response_types,
                redirect_uris=client_record.redirect_uris,
                scope=client_record.scope,
            )

    async def get_authorization_code(
        self, request: Request, client_id: str, code: str
    ) -> Optional[AuthorizationCode]:
        q_results = await self.database.select(
            select(AuthorizationCodeDB).where(AuthorizationCodeDB.code == code)
        )

        authorization_code_record: Optional[AuthorizationCode]
        authorization_code_record = q_results.one_or_none()

        if authorization_code_record is not None:
            return AuthorizationCode(
                code=authorization_code_record.code,
                client_id=authorization_code_record.client_id,
                redirect_uri=authorization_code_record.redirect_uri,
                response_type=authorization_code_record.response_type,
                scope=authorization_code_record.scope,
                auth_time=authorization_code_record.auth_time,
                expires_in=authorization_code_record.expires_in,
                code_challenge=authorization_code_record.code_challenge,
                code_challenge_method=authorization_code_record.code_challenge_method,
                nonce=authorization_code_record.nonce,
            )

    async def delete_authorization_code(
        self, request: Request, client_id: str, code: str
    ) -> None:
        q_results = await self.database.select(
            select(AuthorizationCodeDB).where(AuthorizationCodeDB.code == code)
        )

        authorization_code: Optional[AuthorizationCodeDB]
        authorization_code = q_results.one_or_none()

        await self.database.delete(authorization_code)
