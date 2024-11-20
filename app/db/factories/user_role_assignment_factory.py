from typing import List
from faker import Faker
from app.models import UserRoleAssignment

fake = Faker()


class UserRoleAssignmentFactory():
    _id_counter = 1

    @classmethod
    def _get_next_id(cls):
        current_id = cls._id_counter
        cls._id_counter += 1
        return current_id

    @classmethod
    def create(cls, db_session, **kwargs) -> UserRoleAssignment:
        current_id = cls._get_next_id()
        fake_user_role_assignment = UserRoleAssignment(
            assignment_id=kwargs.get("assignment_id", current_id),
            user_id=kwargs.get("user_id", current_id),
            role_id=kwargs.get("role_id", current_id),
        )
        db_session.add(fake_user_role_assignment)
        db_session.commit()
        return fake_user_role_assignment

    @classmethod
    def batch_create(cls, db_session, size=10, **kwargs) -> List[UserRoleAssignment]:
        assignments = []
        for _ in range(size):
            assignments.append(
                cls.create(db_session, **kwargs)
            )
        return assignments
