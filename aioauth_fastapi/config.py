from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "AIOAuth FastAPI example"
    PROJECT_HOST: str = "0.0.0.0"
    PROJECT_PORT: int = 8001
    DEBUG: bool = False

    REDIS_DSN: str
    PSQL_DSN: str

    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str

    ACCESS_TOKEN_EXP: int = 900  # 15 minutes
    REFRESH_TOKEN_EXP: int = 86400  # 1 day

    AIOAUTH_TOKEN_EXPIRES_IN: Optional[int] = None
    AIOAUTH_AUTHORIZATION_CODE_EXPIRES_IN: Optional[int] = None
    AIOAUTH_INSECURE_TRANSPORT: Optional[bool] = None
    AIOAUTH_ERROR_URI: Optional[str] = None
    AIOAUTH_AVAILABLE: Optional[bool] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
