from typing import List
from aioauth.types import GrantType, ResponseType
from pydantic import BaseModel


class ClientCreate(BaseModel):
    client_id: str
    client_secret: str
    grant_types: List[GrantType]
    response_types: List[ResponseType]
    redirect_uris: List[str]
    scope: str
