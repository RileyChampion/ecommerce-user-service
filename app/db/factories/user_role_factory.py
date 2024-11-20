from typing import List
from faker import Faker
from app.models import UserRole

fake = Faker()


class UserRoleFactory():
    _id_counter = 1

    @classmethod
    def _get_next_id(cls) -> int:
        current_id = cls._id_counter
        cls._id_counter += 1
        return current_id

    @classmethod
    def create(cls, db_session, **kwargs) -> UserRole:
        fake_role = UserRole(
            role_id=kwargs.get("role_id", cls._get_next_id()),
            role_name=kwargs.get("role_name", fake.job())
        )
        db_session.add(fake_role)
        db_session.commit()
        return fake_role

    @classmethod
    def batch_create(cls, db_session, size=10, **kwargs) -> List[UserRole]:
        user_roles = []
        for _ in range(size):
            user_roles.append(cls.create(db_session, **kwargs))
        return user_roles
