from pydantic import BaseModel, PositiveInt


class UserAddressBase(BaseModel):
    address_line1: str
    address_line2: str
    city: str
    state: str
    zip_code: PositiveInt
    country_code: PositiveInt


class UserAddressCreate(UserAddressBase):
    user_id: int


class UserAddressInfoUpdate(UserAddressBase):
    is_primary: bool


class UserAddressResponse(UserAddressBase):
    address_id: int

    class Config:
        orm_mode = True
