from fastapi import FastAPI
from fastapi.param_functions import Security
from fastapi.responses import ORJSONResponse
from starlette.middleware.authentication import AuthenticationMiddleware
from fastapi.security import APIKeyHeader

from .config import settings
from .containers import ApplicationContainer
from .oauth2 import endpoints as oauth2_endpoints
from .users import endpoints as users_endpoints
from .admin.users import endpoints as admin_users_endpoints
from .admin.oauth2 import endpoints as oauth2_admin_endpoints
from .users.backends import TokenAuthenticationBackend

api_key_header = APIKeyHeader(name="authorization", auto_error=False)

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

app.container = ApplicationContainer()
app.container.init_resources()
app.container.wire(
    modules=[
        oauth2_endpoints,
        users_endpoints,
        admin_users_endpoints,
        oauth2_admin_endpoints,
    ]
)

# Include API router
app.include_router(users_endpoints.router, prefix="/api/users", tags=["users"])
app.include_router(
    admin_users_endpoints.routers,
    prefix="/api/admin/users",
    tags=["admin"],
    dependencies=[Security(api_key_header)],
)
app.include_router(
    oauth2_admin_endpoints.routers,
    prefix="/api/admin/oauth2",
    tags=["admin"],
    dependencies=[Security(api_key_header)],
)

# Define aioauth-fastapi endpoints
app.include_router(
    oauth2_endpoints.get_router(),
    prefix="/oauth2",
    tags=["oauth2"],
)

app.add_middleware(AuthenticationMiddleware, backend=TokenAuthenticationBackend())
