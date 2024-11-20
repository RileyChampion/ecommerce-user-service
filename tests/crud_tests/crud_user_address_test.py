from app.crud.user_address import (
    get_all_addresses,
    get_address_address_id,
    update_address_info,
    update_address_toggle_is_primary,
    delete_address
)
from app.models.users import User
from app.schemas.user import UserCreate, UserInfoUpdate, UserPasswordUpdate