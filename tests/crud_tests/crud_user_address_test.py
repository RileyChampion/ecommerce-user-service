import pytest
from app.crud.user_address import (
    get_all_addresses,
    get_address_address_id,
    create_address,
    update_address_info,
    update_address_toggle_is_primary,
    delete_address
)
from app.models.user_addresses import UserAddress
from app.schemas.user_address import UserAddressCreate, UserAddressInfoUpdate, UserAddressToggleIsPrimary


def test_get_all_addresses(db_session, batch_create_addresses):
    batch_create_addresses(10)
    addresses = get_all_addresses(db_session)
    assert len(addresses) == 10

def test_get_address(db_session, create_address):
    test_address = create_address(
        address_id=1000
    )
    address = get_address_address_id(db_session, test_address.address_id)

    assert address.address_id == 1000


def test_create_address(db_session):
    creator_address = UserAddressCreate(
        user_id=20,
        address_line1="Sample Address Line Rd",
        address_line2="Apt 2",
        city="NYC",
        state="NY",
        zip_code=12939,
        country_code="DS",
        is_primary=False
    )

    created_address = create_address(db_session, creator_address)

    assert created_address.user_id == 20
    assert created_address.address_line1 == "Sample Address Line Rd"
    assert created_address.address_line2 == "Apt 2"
    assert created_address.city == "NYC"
    assert created_address.state == "NY"
    assert created_address.zip_code == 12939
    assert created_address.country_code == "DS"
    assert created_address.is_primary == False


def test_update_address_info(db_session, create_address):
    test_address = create_address(
        address_line1="Replace This Address"
    )

    updater_address_info = UserAddressInfoUpdate(
        address_line1="New Address Line",
        address_line2=test_address.address_line2,
        city=test_address.city,
        state=test_address.state,
        zip_code=test_address.zip_code,
        country_code=test_address.country_code,
        is_primary=False
    )

    updated_address = update_address_info(db_session, test_address.address_id, updater_address_info)

    assert updated_address.address_line1 == "New Address Line"

def test_test_update_address_info_not_found(db_session):
    updater_address_info = UserAddressInfoUpdate(
        address_line1="Sample Address Line Rd",
        address_line2="Apt 2",
        city="NYC",
        state="NY",
        zip_code=12939,
        country_code="DS",
        is_primary=False
    )

    with pytest.raises(ValueError) as exec_info:
        update_address_info(db_session, 33, updater_address_info)
    
    assert exec_info.value.args[0] == "Address not found."


def test_update_address_toggle_is_primary(db_session, create_address):
    test_address = create_address(
        is_primary=False
    )

    updater_address_info_toggle = UserAddressToggleIsPrimary(
        is_primary=True
    )

    updated_address = update_address_toggle_is_primary(db_session, test_address.address_id, updater_address_info_toggle)

    assert updated_address.is_primary == True

def test_update_address_toggle_is_primary_not_found(db_session):
    updater_address_info_toggle = UserAddressToggleIsPrimary(
        is_primary=True
    )
    with pytest.raises(ValueError) as exec_info:
        update_address_toggle_is_primary(db_session, 33, updater_address_info_toggle)
    
    assert exec_info.value.args[0] == "Address not found."


def test_delete_address(db_session, create_address):
    test_address = create_address(
        id = 250
    )

    delete_address(db_session, test_address.address_id)
    db_session.commit()

    deleted_address = db_session.query(UserAddress).filter(
        UserAddress.address_id == 250
    ).first()

    assert deleted_address is None

def test_delete_address_not_found(db_session):
    with pytest.raises(ValueError) as exec_info:
        delete_address(db_session, 500)
    
    assert exec_info.value.args[0] == "Address not found."