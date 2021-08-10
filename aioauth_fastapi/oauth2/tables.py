from sqlalchemy.dialects.postgresql import ARRAY
from ..storage.tables import BaseTable


from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
)


class ClientTable(BaseTable):
    __tablename__ = "client"

    client_id = Column(String)
    client_secret = Column(String)
    grant_types = Column(ARRAY(String))
    response_types = Column(ARRAY(String))
    redirect_uris = Column(ARRAY(String))
    scope = Column(String)


class AuthorizationCodeTable(BaseTable):
    __tablename__ = "authorization_code"

    code = Column(String)
    client_id = Column(String)
    redirect_uri = Column(String)
    response_type = Column(String)
    scope = Column(String)
    auth_time = Column(Integer)
    expires_in = Column(Integer)
    code_challenge = Column(String)
    code_challenge_method = Column(String)
    nonce = Column(String)


class TokenTable(BaseTable):
    __tablename__ = "token"

    access_token = Column(String)
    refresh_token = Column(String)
    scope = Column(String)
    issued_at = Column(Integer)
    expires_in = Column(Integer)
    client_id = Column(String)
    token_type = Column(String)
    revoked = Column(Boolean)
