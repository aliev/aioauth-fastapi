from fastapi import FastAPI
from fastapi.param_functions import Security
from fastapi.responses import ORJSONResponse
from starlette.middleware.authentication import AuthenticationMiddleware
from fastapi.security import APIKeyHeader

from .config import settings
from .oauth2 import endpoints as oauth2_endpoints
from .users import endpoints as users_endpoints
from .admin import endpoints as admin_endpoints
from .users.backends import TokenAuthenticationBackend
from .events import on_shutdown, on_startup

api_key_header = APIKeyHeader(name="authorization", auto_error=False)

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    on_startup=on_startup,
    on_shutdown=on_shutdown,
)

# Include API router
app.include_router(users_endpoints.router, prefix="/api/users", tags=["users"])
app.include_router(
    admin_endpoints.routers,
    prefix="/api/admin",
    tags=["admin"],
    dependencies=[Security(api_key_header)],
)

# Define aioauth-fastapi endpoints
app.include_router(
    oauth2_endpoints.router,
    prefix="/oauth2",
    tags=["oauth2"],
)

app.add_middleware(AuthenticationMiddleware, backend=TokenAuthenticationBackend())
