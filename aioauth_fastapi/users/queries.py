from dataclasses import dataclass

from fastapi.params import Query


@dataclass
class AuthorizationCodeQuery:
    code: str = Query(...)
    scope: str = Query(None)
