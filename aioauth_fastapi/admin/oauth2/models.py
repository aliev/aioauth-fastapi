from typing import List, Optional
from aioauth.types import GrantType, ResponseType
from pydantic import BaseModel


class ClientCreate(BaseModel):
    client_id: str
    client_secret: str
    grant_types: List[GrantType]
    response_types: List[ResponseType]
    redirect_uris: List[str]
    scope: str


class ClientUpdate(BaseModel):
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    grant_types: Optional[List[GrantType]] = None
    response_types: Optional[List[ResponseType]] = None
    redirect_uris: Optional[List[str]] = None
    scope: Optional[str] = None
