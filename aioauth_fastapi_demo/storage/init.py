from aioauth_fastapi_demo.storage.sqlalchemy import SQLAlchemy
from aioauth_fastapi_demo.config import settings


database = SQLAlchemy(settings.PSQL_DSN)

def get_database() -> SQLAlchemy:
    return database
