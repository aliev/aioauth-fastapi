import uvicorn

from aioauth_fastapi.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "aioauth_fastapi.app:app",
        host=settings.PROJECT_HOST,
        port=settings.PROJECT_PORT,
        reload=settings.DEBUG,
    )
