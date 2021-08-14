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

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
