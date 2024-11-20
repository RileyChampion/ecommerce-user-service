import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base
from app.core.dependencies import get_db
from app.main import app
from fastapi.testclient import TestClient
from app.db.factories.user_role_factory import UserRoleFactory
from app.db.factories.user_factory import UserFactory

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

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
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()