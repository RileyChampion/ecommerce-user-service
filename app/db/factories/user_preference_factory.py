from typing import List
from faker import Faker
from app.models import UserPreference

fake = Faker()


class UserPreferenceFactory():
    _id_counter = 1

    @classmethod
    def _get_next_id(cls) -> int:
        current_id = cls._id_counter
        cls._id_counter += 1
        return current_id

    @classmethod
    def create(cls, db_session, **kwargs) -> UserPreference:
        current_id = cls._get_next_id()
        fake_user_preference = UserPreference(
            preference_id=kwargs.get(
                "preference_id",
                current_id
            ),
            user_id=kwargs.get("user_id", current_id),
            preference_type=kwargs.get(
                "preference_type",
                fake.company()
            ),
            preference_value=kwargs.get(
                "preference_value",
                fake.random_letter()
            )
        )
        db_session.add(fake_user_preference)
        db_session.commit()
        return fake_user_preference

    @classmethod
    def batch_create(cls, db_session, size=10, **kwargs) -> List[UserPreference]:
        user_preferences = []
        for _ in range(size):
            user_preferences.append(
                cls.create(db_session, **kwargs)
            )
        return user_preferences
