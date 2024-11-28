from sqlalchemy.orm import Session
from app.db.factories.user_address_factory import UserAddressFactory


def test_user_address_factory_create(db_session: Session, create_user):
    user = create_user()
    address = UserAddressFactory.create(
        db_session,
        user_id=user.id,
        address_line1="Test Address1 Lane"
    )
    assert address.address_line1 == "Test Address1 Lane"
    assert address.user_id == user.id


def test_user_address_factory_batch_create(db_session: Session):
    roles = UserAddressFactory.batch_create(
        db_session,
        size=10
    )
    assert len(roles) == 10