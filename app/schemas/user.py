from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    telephone: str
    profile_pic: str


class UserCreate(UserBase):
    password: str
    profile_pic: str


class UserInfoUpdate(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    telephone: str
    profile_pic: str
    is_active: bool


class UserPasswordUpdate(BaseModel):
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
