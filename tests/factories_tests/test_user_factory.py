from sqlalchemy.orm import Session
from app.db.factories.user_factory import UserFactory


def test_user_factory_create(db_session: Session, use_verify_password):
    user = UserFactory.create(
        db_session,
        username="test_username",
        first_name="John",
        last_name="Doe",
        hashed_password="secure_password"
    )
    assert user.username == "test_username"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert use_verify_password("secure_password", user.hashed_password) is True


def test_user_factory_batch_create(db_session: Session):
    users = UserFactory.batch_create(
        db_session,
        size=5
    )
    assert len(users) == 5
