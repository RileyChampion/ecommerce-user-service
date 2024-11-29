from typing import List
from app.models.users import User

from app.db.session import Base, engine, SessionLocal
from app.db.factories.user_factory import UserFactory
from app.db.factories.user_role_factory import UserRoleFactory
from app.db.factories.user_address_factory import UserAddressFactory
from app.db.factories.user_preference_factory import UserPreferenceFactory
from app.db.factories.user_role_assignment_factory import UserRoleAssignmentFactory

def create_db():
    Base.metadata.create_all(bind=engine)
    print("Database created!")

    # Seed the database with initial data (optional)
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()

def seed_data(db):
    # Create User Roles
    admin = UserRoleFactory.create(db, role_name="Admin")
    customer = UserRoleFactory.create(db, role_name="Customer")
    
    # Create Users
    users: List[User] = UserFactory.batch_create(db, 30)

    test_user: User = UserFactory.create(
        db,
        username="test_user",
        hashed_password="password"
    )
    users.append(test_user)

    # Create User Addresses, Preferences and Role Assignment
    for user in users:
        UserAddressFactory.create(db, user_id=user.id)
        UserPreferenceFactory.create(db, user_id=user.id)
        if user.id % 10 == 0 or user.id == 31:
            UserRoleAssignmentFactory.create(db, user_id=user.id, role_id=admin.role_id)
        else:
            UserRoleAssignmentFactory.create(db, user_id=user.id, role_id=customer.role_id)

if __name__ == '__main__':
    create_db()