from fastapi import APIRouter
from aioauth_fastapi.api.users.endpoints import router as users_router

api_router = APIRouter()

api_router.include_router(users_router, prefix="/users", tags=["users"])
