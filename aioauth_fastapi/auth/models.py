from pydantic import BaseModel


class AnonymousUser(BaseModel):
    is_authenticated: bool = False
    is_superuser: bool = False


class User(BaseModel):
    id: str
    is_superuser: bool
    is_blocked: bool
    username: str
    is_authenticated: bool = True

    class Config:
        orm_mode = True
