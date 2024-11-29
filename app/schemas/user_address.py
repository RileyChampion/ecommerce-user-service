from pydantic import BaseModel


class UserAddressBase(BaseModel):
    address_line1: str
    address_line2: str
    city: str
    state: str
    zip_code: int
    country_code: str


class UserAddressCreate(UserAddressBase):
    user_id: int
    is_primary: bool


class UserAddressInfoUpdate(UserAddressBase):
    is_primary: bool


class UserAddressToggleIsPrimary(BaseModel):
    is_primary: bool


class UserAddressResponse(UserAddressBase):
    is_primary: bool

    class Config:
        orm_mode = True
