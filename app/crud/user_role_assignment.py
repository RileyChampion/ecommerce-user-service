from typing import List, Union
from sqlalchemy.orm import Session
from app.models.user_role_assignments import UserRoleAssignment
from app.schemas.user_role_assignment import UserRoleAssignmentCreate


def create_role_assignment(db: Session, created_assignment: UserRoleAssignmentCreate):
    created_assignment = UserRoleAssignment(
        role_id=created_assignment.role_id,
        user_id=created_assignment.user_id
    )

    db.add(created_assignment)
    return created_assignment


def delete_role_assignment_assignment_id(db: Session, assignment_id: int):
    deleting_assignment = db.query(UserRoleAssignment).filter(
        UserRoleAssignment.assignment_id == assignment_id
    ).first()

    if not deleting_assignment:
        raise ValueError("Role Assignment not found.")

    db.delete(deleting_assignment)


def delete_role_assignment_role_id_user_id(db: Session, role_id: int, user_id: int):
    deleting_assignment = db.query(UserRoleAssignment).filter(
        UserRoleAssignment.role_id == role_id,
        UserRoleAssignment.user_id == user_id
    ).first()

    if not deleting_assignment:
        raise ValueError("Role Assignment not found.")
    
    db.delete(deleting_assignment)