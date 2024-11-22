from typing import List
from sqlalchemy.orm import Session
from app.models.user_addresses import UserAddress
from app.schemas.user_address import (
    UserAddressCreate,
    UserAddressInfoUpdate,
    UserAddressToggleIsPrimary
)


def get_all_addresses(db: Session) -> List[UserAddress]:
    return db.query(UserAddress).all()


def get_address_address_id(db: Session, address_id: int) -> UserAddress:
    return db.query(UserAddress).filter(
        UserAddress.address_id == address_id
    ).first()


def create_address(db: Session, address: UserAddressCreate) -> UserAddressCreate:
    created_address = UserAddress(
        user_id=address.user_id,
        address_line1=address.address_line1,
        address_line2=address.address_line2,
        city=address.city,
        state=address.state,
        zip_code=address.zip_code,
        country_code=address.country_code,
        is_primary=address.is_primary
    )
    return created_address


def update_address_info(db: Session, address_id: int, address: UserAddressInfoUpdate):
    found_address = db.query(UserAddress).filter(
        UserAddress.address_id == address_id
    ).first()

    if not found_address:
        raise ValueError("Address not found.")

    found_address.address_line1 = address.address_line1
    found_address.address_line2 = address.address_line2
    found_address.city = address.city
    found_address.state = address.state
    found_address.zip_code = address.zip_code
    found_address.country_code = address.country_code
    found_address.is_primary = address.is_primary

    return found_address


def update_address_toggle_is_primary(db: Session, address_id: int, address: UserAddressToggleIsPrimary):
    found_address = db.query(UserAddress).filter(
        UserAddress.address_id == address_id
    ).first()

    if not found_address:
        raise ValueError("Address not found.")

    found_address.is_primary = address.is_primary

    return found_address


def delete_address(db: Session, address_id: int) -> None:
    found_address = db.query(UserAddress).filter(
        UserAddress.address_id == address_id
    ).first()

    if not found_address:
        raise ValueError("Address not found.")

    db.delete(found_address)
