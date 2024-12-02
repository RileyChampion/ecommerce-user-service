import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base
from app.core.dependencies import get_db
from app.main import app
from fastapi.testclient import TestClient
from app.models.users import User
from app.db.factories.user_role_factory import UserRoleFactory
from app.db.factories.user_factory import UserFactory
from app.db.factories.user_address_factory import UserAddressFactory
from app.db.factories.user_preference_factory import UserPreferenceFactory
from app.db.factories.user_role_assignment_factory import UserRoleAssignmentFactory
from app.core.security import verify_password, get_current_user

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# DB Session
@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


# Factories - Single
@pytest.fixture
def create_user(db_session):
    def _create_user(**kwargs):
        return UserFactory.create(db_session, **kwargs)
    return _create_user


@pytest.fixture
def create_role(db_session):
    def _create_role(**kwargs):
        return UserRoleFactory.create(db_session, **kwargs)
    return _create_role


@pytest.fixture
def create_address(db_session):
    def _create_address(**kwargs):
        return UserAddressFactory.create(db_session, **kwargs)
    return _create_address


@pytest.fixture
def create_preference(db_session):
    def _create_preference(**kwargs):
        return UserPreferenceFactory.create(db_session, **kwargs)
    return _create_preference


@pytest.fixture
def create_role_assignment(db_session):
    def _create_role_assignment(**kwargs):
        return UserRoleAssignmentFactory.create(db_session, **kwargs)
    return _create_role_assignment


# Factories - Batch
@pytest.fixture
def batch_create_users(db_session):
    def _batch_create_users(size=10, **kwargs):
        return UserFactory.batch_create(db_session, size, **kwargs)
    return _batch_create_users


@pytest.fixture
def batch_create_roles(db_session):
    def _batch_create_roles(size=10, **kwargs):
        return UserRoleFactory.batch_create(db_session, size, **kwargs)
    return _batch_create_roles


@pytest.fixture
def batch_create_addresses(db_session):
    def _batch_create_addresses(size=10, **kwargs):
        return UserAddressFactory.batch_create(db_session, size, **kwargs)
    return _batch_create_addresses


@pytest.fixture
def batch_create_preferences(db_session):
    def _batch_create_preferences(size=10, **kwargs):
        return UserPreferenceFactory.batch_create(db_session, size, **kwargs)
    return _batch_create_preferences


# Test Client
@pytest.fixture
def client():
    def override_get_db():
        Base.metadata.create_all(bind=engine)
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
            Base.metadata.drop_all(bind=engine)
    
    def override_get_current_user():
        return User(
            id=100,
            username="test_user_name",
            first_name="John",
            last_name="Doe",
            email="example@email.com",
            telephone="757-348-5869",
            hashed_password="super_strong_password"
        )

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    # print(app.routes)
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# Verifying Passwords
@pytest.fixture
def use_verify_password():
    def _use_verify_password(plain_pass: str, hashed_pass: str):
        return verify_password(plain_pass, hashed_pass)
    return _use_verify_password


@pytest.fixture
def retrieve_test_oauth_token():
    return "fake_token"
