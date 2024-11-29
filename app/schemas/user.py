from typing import List
from pydantic import BaseModel, EmailStr
from app.schemas.user_address import UserAddressResponse
from app.schemas.user_preference import UserPreferenceResponse
from app.schemas.user_role import UserRoleResponse


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


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserResponseWithRelaltionships(UserBase):
    id: int
    addresses: List[UserAddressResponse]
    preferences: List[UserPreferenceResponse]
    roles: List[UserRoleResponse]

    class Config:
        orm_mode = True
