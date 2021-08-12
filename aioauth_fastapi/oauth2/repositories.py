from typing import Optional
from aioauth_fastapi.storage.db import Database
from aioauth.requests import Request
from aioauth.models import Token, AuthorizationCode, Client
from .tables import ClientTable, TokenTable, AuthorizationCodeTable
from sqlalchemy.future import select
from aioauth.storage import BaseStorage


class OAuth2Repository(BaseStorage):
    def __init__(self, database: Database):
        self.database = database

    async def save_token(self, token: Token) -> None:
        token_record = TokenTable(**token._asdict())

        async with self.database.session() as session:
            session.add(token_record)
            await session.commit()

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
        authorization_code_record = AuthorizationCodeTable(
            **authorization_code._asdict()
        )

        async with self.database.session() as session:
            session.add(authorization_code_record)
            await session.commit()

    async def get_client(
        self, request: Request, client_id: str, client_secret: Optional[str] = None
    ) -> Optional[Client]:
        q = select(ClientTable).where(ClientTable.client_id == client_id)
        async with self.database.session() as session:
            results = await session.execute(q)
            one = results.scalars().one_or_none()

        if one is not None:
            return Client(
                client_id=one.client_id,
                client_secret=one.client_secret,
                grant_types=one.grant_types,
                response_types=one.response_types,
                redirect_uris=one.redirect_uris,
                scope=one.scope,
            )

    async def authenticate(self, request: Request) -> bool:
        return await super().authenticate(request)

    async def get_authorization_code(
        self, request: Request, client_id: str, code: str
    ) -> Optional[AuthorizationCode]:
        q = select(AuthorizationCodeTable).where(AuthorizationCodeTable.code == code)

        async with self.database.session() as session:
            results = await session.execute(q)
            one = results.scalars().one_or_none()

        if one is not None:
            return AuthorizationCode(
                code=one.code,
                client_id=one.client_id,
                redirect_uri=one.redirect_uri,
                response_type=one.response_type,
                scope=one.scope,
                auth_time=one.auth_time,
                expires_in=one.expires_in,
                code_challenge=one.code_challenge,
                code_challenge_method=one.code_challenge_method,
                nonce=one.nonce,
            )

    async def delete_authorization_code(
        self, request: Request, client_id: str, code: str
    ) -> None:
        q = select(AuthorizationCodeTable).where(AuthorizationCodeTable.code == code)

        async with self.database.session() as session:
            results = await session.execute(q)
            one = results.scalars().one_or_none()

            await session.delete(one)
            await session.commit()

    async def revoke_token(self, request: Request, refresh_token: str) -> None:
        return await super().revoke_token(request, refresh_token)
