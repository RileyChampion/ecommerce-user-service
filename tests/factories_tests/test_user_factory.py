from sqlalchemy.orm import Session
from app.db.factories.user_factory import UserFactory


def test_user_factory_create(db_session: Session):
    user = UserFactory.create(
        db_session,
        username="test_username",
        full_name="John Doe",
        password="secure_password"
        )
    assert user.username == "test_username"
    assert user.full_name == "John Doe"
    assert user.password == "secure_password"

def test_user_factory_batch_create(db_session: Session):
    users = UserFactory.batch_create(
        db_session,
        size=5
        )
    assert len(users) == 5
