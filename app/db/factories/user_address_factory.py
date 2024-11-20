from typing import List
from faker import Faker
from app.models import UserAddress

fake = Faker()


class UserAddressFactory():
    _id_counter = 1

    @classmethod
    def _get_next_id(cls) -> int:
        current_id = cls._id_counter
        cls._id_counter += 1
        return current_id

    @classmethod
    def create(cls, db_session, **kwargs) -> UserAddress:
        current_id = cls._get_next_id()
        fake_user_address = UserAddress(
            address_id=kwargs.get("address_id", current_id),
            user_id=kwargs.get("user_id", current_id),
            address_line1=kwargs.get("address_line1", fake.street_address()),
            address_line2=kwargs.get("address_line2", None),
            city=kwargs.get("city", fake.city()),
            state=kwargs.get("state", fake.state()),
            zip_code=kwargs.get("zip_code", fake.zipcode()),
            country_code=kwargs.get("country_code", fake.country_code()),
            is_primary=kwargs.get("is_primary", False)
        )
        db_session.add(fake_user_address)
        db_session.commit()
        return fake_user_address

    @classmethod
    def batch_create(cls, db_session, size=10, **kwargs) -> List[UserAddress]:
        user_addresses = []
        for _ in range(size):
            user_addresses.append(
                UserAddressFactory.create(db_session, **kwargs)
            )
        return user_addresses
