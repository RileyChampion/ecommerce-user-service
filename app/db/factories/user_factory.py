from typing import List
from faker import Faker
from app.models import User

fake = Faker()


class UserFactory:
    _id_counter = 1

    @classmethod
    def _get_next_id(cls) -> int:
        current_id = cls._id_counter
        cls._id_counter += 1
        return current_id

    @classmethod
    def create(cls, db_session, **kwargs) -> User:
        fake_user = User(
            id=kwargs.get("id", cls._get_next_id()),
            username=kwargs.get("username", fake.user_name()),
            first_name=kwargs.get("first_name", fake.first_name()),
            last_name=kwargs.get("last_name", fake.last_name()),
            email=kwargs.get("email", fake.email()),
            telephone=kwargs.get("telephone", fake.phone_number()),
            password=kwargs.get("password", fake.password()),
            profile_pic=kwargs.get("profile_pic", "default.png"),
            is_active=kwargs.get("profile_pic", False)
        )
        db_session.add(fake_user)
        db_session.commit()
        return fake_user

    @classmethod
    def batch_create(cls, db_session, size=10, **kwargs) -> List[User]:
        users = []
        for _ in range(size):
            users.append(cls.create(db_session, **kwargs))
        return users
