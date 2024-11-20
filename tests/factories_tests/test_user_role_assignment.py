from sqlalchemy.orm import Session
from app.db.factories.user_role_assignment_factory import UserRoleAssignmentFactory


def test_user_role_assignment_factory_create(db_session: Session, create_user, create_role):
    test_user = create_user()
    test_role = create_role()
    assignment = UserRoleAssignmentFactory.create(
        db_session,
        user_id=test_user.id,
        role_id=test_role.role_id
    )
    assert assignment.user_id == test_user.id
    assert assignment.role_id == test_role.role_id

def test_user_address_factory_batch_create(db_session: Session):
    roles = UserRoleAssignmentFactory.batch_create(
        db_session,
        size=5
        )
    assert len(roles) == 5