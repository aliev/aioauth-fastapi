from fastapi import FastAPI, Security
from fastapi.responses import ORJSONResponse
from fastapi.security import APIKeyHeader
from aioauth_fastapi.auth.backends import JWTAuthBackend
from aioauth_fastapi.events import on_shutdown, on_startup
from aioauth_fastapi.config import settings

from .containers import ApplicationContainer

from .users import endpoints as users_endpoint

from starlette.middleware.authentication import AuthenticationMiddleware

api_key = APIKeyHeader(name="authorization", auto_error=False)

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    on_startup=on_startup,
    on_shutdown=on_shutdown,
)

container = ApplicationContainer()
app.container = container
app.container.init_resources()
app.container.wire(modules=[users_endpoint])


# Include API router
app.include_router(
    users_endpoint.router, prefix="/api/users", dependencies=[Security(api_key)]
)
app.add_middleware(AuthenticationMiddleware, backend=JWTAuthBackend())
