from pydantic import BaseModel


class BaseUser(BaseModel):
    @property
    def is_authenticated(self):
        return False

    @property
    def is_superuser(self):
        return False


class AnonymousUser(BaseUser):
    pass


class User(BaseModel):
    id: str
    is_superuser: bool
    is_blocked: bool
    username: str

    @property
    def is_authenticated(self):
        return True

    class Config:
        orm_mode = True
