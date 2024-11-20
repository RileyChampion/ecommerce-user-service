from app.crud.user import (
    get_all_users,
    get_user,
    create_user,
    update_user_info,
    update_user_password,
    delete_user
)
from app.models.users import User
from app.schemas.user import UserCreate, UserInfoUpdate, UserPasswordUpdate


def test_get_all_users(db_session, batch_create_users):
    batch_create_users(10)
    users = get_all_users(db_session)
    assert len(users) == 10


def test_get_user(db_session, create_user):
    test_user = create_user(
        id=1000
    )
    user = get_user(db_session, test_user.id)
    assert user.id == test_user.id


def test_create_user(db_session):
    test_create = UserCreate(
        username="usernameTest",
        first_name="John",
        last_name="Doe",
        email="testemail@gmail.com",
        telephone="123-312-5543",
        password="super_strong_password",
        profile_pic="default.png"
    )
    created_user = create_user(db_session, test_create)
    
    assert created_user.username == "usernameTest"
    assert created_user.first_name == "John"
    assert created_user.last_name == "Doe"
    assert created_user.email == "testemail@gmail.com"
    assert created_user.telephone == "123-312-5543"
    assert created_user.password == "super_strong_password"
    assert created_user.profile_pic == "default.png"


def test_update_user_info(db_session, create_user):
    test_user = create_user(
        username="ChangeThisName"
    )

    update_info = UserInfoUpdate(
        username="NewUserName",
        first_name=test_user.first_name,
        last_name=test_user.last_name,
        email=test_user.email,
        telephone=test_user.telephone,
        profile_pic=test_user.profile_pic,
        is_active=test_user.is_active
    )

    updated_user = update_user_info(db_session, test_user.id, update_info)

    assert updated_user.username == "NewUserName"


def test_update_user_password(db_session, create_user):
    test_user = create_user(
        password="weakpassword"
    )

    update_password = UserPasswordUpdate(
        password="N3WsTr0nGP4sSw0rD"
    )

    updated_user = update_user_password(db_session, test_user.id, update_password)

    assert updated_user.password == "N3WsTr0nGP4sSw0rD"

def test_delete_user(db_session, create_user):
    test_user = create_user(
        id=250
    )

    delete_user(db_session, test_user.id)
    db_session.commit()

    deleted_user = db_session.query(User).filter(User.id == 250).first()
    assert deleted_user is None
