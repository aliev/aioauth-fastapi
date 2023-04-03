"""
.. code-block:: python

    from aioauth_fastapi import router

FastAPI routing of oauth2.

Usage example

.. code-block:: python

    from aioauth_fastapi.router import get_oauth2_router
    from aioauth.storage import BaseStorage
    from aioauth.config import Settings
    from aioauth.server import AuthorizationServer
    from fastapi import FastAPI

    app = FastAPI()

    class SQLAlchemyCRUD(BaseStorage):
        '''
        SQLAlchemyCRUD methods must be implemented here.
        '''

    # NOTE: Redefinition of the default aioauth settings
    # INSECURE_TRANSPORT must be enabled for local development only!
    settings = Settings(
        INSECURE_TRANSPORT=True,
    )

    storage = SQLAlchemyCRUD()
    authorization_server = AuthorizationServer(storage)

    # Include FastAPI router with oauth2 endpoints.
    app.include_router(
        get_oauth2_router(authorization_server, settings),
        prefix="/oauth2",
        tags=["oauth2"],
    )

----
"""

from typing import Callable, TypeVar

from aioauth.config import Settings
from aioauth.requests import TRequest
from aioauth.server import AuthorizationServer
from aioauth.storage import TStorage
from fastapi import APIRouter, Request

from .utils import (
    RequestArguments,
    default_request_factory,
    to_fastapi_response,
    to_oauth2_request,
)


ARequest = TypeVar("ARequest", bound=TRequest)


def get_oauth2_router(
    authorization_server: AuthorizationServer[ARequest, TStorage],
    settings: Settings = Settings(),
    request_factory: Callable[[RequestArguments], ARequest] = default_request_factory,
) -> APIRouter:
    """Function will create FastAPI router with the following oauth2 endpoints:

        * POST /token
            * Endpoint creates a token response by :py:meth:`aioauth.server.AuthorizationServer.create_token_response`
        * POST `/token/introspect`
            * Endpoint creates a token introspection by :py:meth:`aioauth.server.AuthorizationServer.create_token_introspection_response`
        * GET `/authorize`
            * Endpoint creates an authorization response by :py:meth:`aioauth.server.AuthorizationServer.create_authorization_response`

    Returns:
        :py:class:`fastapi.APIRouter`.
    """
    router = APIRouter()

    @router.post("/token")
    async def token(request: Request):
        oauth2_request = await to_oauth2_request(
            request=request, request_factory=request_factory, settings=settings
        )
        oauth2_response = await authorization_server.create_token_response(
            oauth2_request
        )
        return await to_fastapi_response(oauth2_response)

    @router.post("/token/introspect")
    async def token_introspect(request: Request):
        oauth2_request = await to_oauth2_request(
            request=request, request_factory=request_factory, settings=settings
        )
        oauth2_response = (
            await authorization_server.create_token_introspection_response(
                oauth2_request
            )
        )
        return await to_fastapi_response(oauth2_response)

    @router.get("/authorize")
    async def authorize(request: Request):
        oauth2_request = await to_oauth2_request(
            request=request, request_factory=request_factory, settings=settings
        )
        oauth2_response = await authorization_server.create_authorization_response(
            oauth2_request
        )
        return await to_fastapi_response(oauth2_response)

    return router
