from pydantic import BaseModel, PositiveInt


class UserRoleBase(BaseModel):
    role_name: str


class UserRoleCreate(BaseModel):
    role_name: str


class UserRoleResponse(UserRoleBase):
    class Config:
        orm_mode = True