"""
.. code-block:: python

    from aioauth_fastapi import utils

Core utils for integration with FastAPI

----
"""

import json
from dataclasses import dataclass
from typing import Callable, Dict, Optional

from aioauth.collections import HTTPHeaderDict
from aioauth.config import Settings
from aioauth.requests import Post, Query, TRequest, TUser
from aioauth.requests import Request as OAuth2Request
from aioauth.responses import Response as OAuth2Response
from fastapi import Request, Response


@dataclass
class RequestArguments:
    headers: HTTPHeaderDict
    method: str
    post_args: Dict
    query_args: Dict
    settings: Settings
    url: str
    user: Optional[TUser]


def default_request_factory(request_args: RequestArguments) -> OAuth2Request:
    return OAuth2Request(
        headers=request_args.headers,
        method=request_args.method,  # type: ignore
        post=Post(**request_args.post_args),  # type: ignore
        query=Query(**request_args.query_args),  # type: ignore
        settings=request_args.settings,
        url=request_args.url,
        user=request_args.user,
    )


async def to_oauth2_request(
    request: Request,
    settings: Settings = Settings(),
    request_factory: Callable[[RequestArguments], TRequest] = default_request_factory,
) -> TRequest:
    """Converts :py:class:`fastapi.Request` instance to :py:class:`aioauth.requests.Request` instance"""
    form = await request.form()

    post_args = dict(form)
    query_args = dict(request.query_params)
    method = request.method
    headers = HTTPHeaderDict(**request.headers)
    url = str(request.url)

    user = None

    if request.user.is_authenticated:
        user = request.user

    request_args = RequestArguments(
        headers=headers,
        method=method,
        post_args=post_args,
        query_args=query_args,
        settings=settings,
        url=url,
        user=user,
    )
    return request_factory(request_args)


async def to_fastapi_response(oauth2_response: OAuth2Response) -> Response:
    """Converts :py:class:`aioauth.responses.Response` instance to :py:class:`fastapi.Response` instance"""
    response_content = oauth2_response.content
    headers = dict(oauth2_response.headers)
    status_code = oauth2_response.status_code
    content = json.dumps(response_content)

    return Response(content=content, headers=headers, status_code=status_code)
