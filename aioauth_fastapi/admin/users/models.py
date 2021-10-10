from pydantic import BaseModel


class UserCreate(BaseModel):
    is_superuser: bool = False
    is_blocked: bool = False
    is_active: bool = False
    username: str
    password: str
