from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class LogoutRequest(BaseModel):
    user_id: int