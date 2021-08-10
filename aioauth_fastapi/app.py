from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from .users.backends import JWTAuthBackend
from .events import on_shutdown, on_startup
from .config import settings

from .containers import ApplicationContainer

from .users import endpoints as users_endpoint
from .oauth2 import endpoints as oauth2_endpoints

from starlette.middleware.authentication import AuthenticationMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    on_startup=on_startup,
    on_shutdown=on_shutdown,
)

app.container = ApplicationContainer()
app.container.init_resources()
app.container.wire(modules=[users_endpoint, oauth2_endpoints])


# Include API router
app.include_router(users_endpoint.router, prefix="/api/users", tags=["users"])
app.include_router(oauth2_endpoints.router, prefix="/api/oauth2", tags=["oauth2"])
app.add_middleware(AuthenticationMiddleware, backend=JWTAuthBackend())
