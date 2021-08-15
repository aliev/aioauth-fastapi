from aioauth.server import AuthorizationServer
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from .users.backends import JWTAuthBackend
from .config import settings
from .containers import ApplicationContainer
from .storage.db import Database
from .users import endpoints as users_endpoint
from .oauth2.storage import OAuth2Storage
from aioauth.config import Settings

from aioauth.fastapi.router import get_oauth2_router

from starlette.middleware.authentication import AuthenticationMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

app.container = ApplicationContainer()
app.container.init_resources()
app.container.wire(modules=[users_endpoint])


database = Database(dsn=settings.PSQL_DSN)


# Include API router
app.include_router(users_endpoint.router, prefix="/api/users", tags=["users"])

# Define aioauth-fastapi endpoints
app.include_router(
    get_oauth2_router(
        AuthorizationServer(storage=OAuth2Storage(database=database)),
        settings=Settings(
            TOKEN_EXPIRES_IN=settings.ACCESS_TOKEN_EXP,
            REFRESH_TOKEN_EXPIRES_IN=settings.REFRESH_TOKEN_EXP,
            INSECURE_TRANSPORT=settings.DEBUG,
        ),
    ),
    prefix="/oauth2",
    tags=["oauth2"],
)

app.add_middleware(AuthenticationMiddleware, backend=JWTAuthBackend())
