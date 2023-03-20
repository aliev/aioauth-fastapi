"""
.. code-block:: python

    from aioauth_fastapi import forms

FastAPI oauth2 forms.

Used to generate an OpenAPI schema.

----
"""

from dataclasses import dataclass
from typing import Optional

from aioauth.types import GrantType, TokenType
from fastapi.params import Form


@dataclass
class TokenForm:
    grant_type: Optional[GrantType] = Form(None)  # type: ignore
    client_id: Optional[str] = Form(None)  # type: ignore
    client_secret: Optional[str] = Form(None)  # type: ignore
    redirect_uri: Optional[str] = Form(None)  # type: ignore
    scope: Optional[str] = Form(None)  # type: ignore
    username: Optional[str] = Form(None)  # type: ignore
    password: Optional[str] = Form(None)  # type: ignore
    refresh_token: Optional[str] = Form(None)  # type: ignore
    code: Optional[str] = Form(None)  # type: ignore
    token: Optional[str] = Form(None)  # type: ignore
    code_verifier: Optional[str] = Form(None)  # type: ignore


@dataclass
class TokenIntrospectForm:
    token: Optional[str] = Form(None)  # type: ignore
    token_type_hint: Optional[TokenType] = Form(None)  # type: ignore
