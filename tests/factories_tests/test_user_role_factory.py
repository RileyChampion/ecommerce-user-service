from sqlalchemy.orm import Session
from app.db.factories.user_role_factory import UserRoleFactory


def test_user_role_factory_create(db_session: Session):
    role = UserRoleFactory.create(
        db_session,
        role_name="Test Role Name"
        )
    assert role.role_name == "Test Role Name"

def test_user_role_factory_batch_create(db_session: Session):
    roles = UserRoleFactory.batch_create(
        db_session,
        size=5
        )
    assert len(roles) == 5
