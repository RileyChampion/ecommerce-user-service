from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    full_name: str | None = None
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: str | None = None
    is_active: bool | None = None

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True