from pydantic import BaseModel, Field
from typing import Literal, Optional


class FilterBase(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"


class UserFilter(FilterBase):
    user_id: Optional[int] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    telephone: Optional[str] = None
    is_active: Literal["true", "false"] = "false"


class UserPreferenceFilter(FilterBase):
    preference_id: Optional[str]
    user_id: Optional[int] = None
    preference_type: Optional[str] = None
    preference_value: Optional[str] = None


class UserRoleFilter(FilterBase):
    role_id: Optional[int] = None
    role_name: Optional[str] = None


class UserAddressFilter(FilterBase):
    address_id: Optional[int] = None
    user_id: Optional[int] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    is_primary: bool
