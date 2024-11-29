import pytest
from app.crud.user_role_assignment import (
    create_role_assignment,
    delete_role_assignment_role_id_user_id
)
from app.models.user_role_assignments import UserRoleAssignment
from app.schemas.user_role_assignment import UserRoleAssignmentCreate


def test_create_role_assignment(db_session):
    test_create = UserRoleAssignmentCreate(
        role_id=1,
        user_id=1
    )

    created_role_assignment = create_role_assignment(db_session, test_create)

    assert created_role_assignment.role_id == test_create.role_id
    assert created_role_assignment.user_id == test_create.user_id


def test_delete_role_assignment_role_id_user_id(db_session, create_role_assignment):
    create_role_assignment(
        role_id=22,
        user_id=3
    )

    delete_role_assignment_role_id_user_id(db_session, 22, 3)
    db_session.commit()

    deleted_role_assignment = db_session.query(UserRoleAssignment).filter(
        UserRoleAssignment.role_id == 22,
        UserRoleAssignment.user_id == 3
    ).first()
    assert deleted_role_assignment is None


def test_delete_role_assignment_role_id_user_id_not_found(db_session):
    with pytest.raises(ValueError) as exec_info:
        delete_role_assignment_role_id_user_id(db_session, 250, 250)
    
    assert exec_info.value.args[0] == "Role Assignment not found."
