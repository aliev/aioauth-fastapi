from dataclasses import dataclass
from typing import Optional
from fastapi.params import Form


@dataclass
class TokenIntrospectRequest:
    token: Optional[str] = Form(None)
