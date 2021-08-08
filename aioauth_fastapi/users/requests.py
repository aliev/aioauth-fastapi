from pydantic import BaseModel


class UserRegistrationRequest(BaseModel):
    username: str
    password: str


class UserLoginRequest(BaseModel):
    username: str
    password: str
