from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    is_superuser: bool = False
    is_blocked: bool = False
    is_active: bool = False
    username: str
    password: str


class UserUpdate(BaseModel):
    is_superuser: Optional[bool] = None
    is_blocked: Optional[bool] = None
    is_active: Optional[bool] = None
    username: Optional[str] = None
    password: Optional[str] = None
