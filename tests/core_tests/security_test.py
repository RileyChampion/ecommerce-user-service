import pytest
import time
import asyncio
from datetime import timedelta, datetime, timezone
from jose import jwt
from fastapi import HTTPException
from app.models.users import User
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token,
    get_current_user,
    authenticate_user,
    login_user,
    TokenData
)


def test_get_password_hash(mocker):
    mocker.patch("passlib.context.CryptContext.hash", return_value="ENCRYPTED_PASSWORD")
    password = "test_password"
    hashed_pass = get_password_hash(password)

    assert password != hashed_pass
    assert hashed_pass == "ENCRYPTED_PASSWORD"


def test_verify_password():
    hashed_pass = get_password_hash("test_password")

    assert verify_password("test_password", hashed_pass) is True


def test_verify_password_different():
    hashed_pass = get_password_hash("different_test_password")

    assert verify_password("test_password", hashed_pass) is False


def test_create_access_token(mocker):
    mock_now = datetime.now(timezone.utc)
    mocked_datetime = mocker.patch("app.core.security.datetime")
    mocker.patch("app.config.settings.SECRET_KEY", "test_secret_key")
    mocker.patch("app.config.settings.ALGORITHM", "HS256")
    # mocker.patch("app.config.settings.ACCESS_TOKEN_EXPIRE_MINUTES", 15)
    mocked_datetime.now.return_value = mock_now

    test_data = {
        "sub": "1234",
        "username": "test_username"
    }

    token = create_access_token(
        data=test_data,
        expires_delta=timedelta(minutes=30)
    )

    decoded_token = jwt.decode(token, "test_secret_key", "HS256")

    test_expires = mock_now + timedelta(minutes=30)

    assert decoded_token["sub"] == "1234"
    assert decoded_token["username"] == "test_username"
    assert "exp" in decoded_token
    assert int(decoded_token["exp"]) == int(test_expires.timestamp())


def test_create_access_token_no_expire_delta(mocker):
    mock_now = datetime.now(timezone.utc)
    mocked_datetime = mocker.patch("app.core.security.datetime")
    mocker.patch("app.config.settings.SECRET_KEY", "test_secret_key")
    mocker.patch("app.config.settings.ALGORITHM", "HS256")
    # mocker.patch("app.config.settings.ACCESS_TOKEN_EXPIRE_MINUTES", 15)
    mocked_datetime.now.return_value = mock_now

    test_data = {
        "sub": "1234",
        "username": "test_username"
    }

    token = create_access_token(
        data=test_data,
        expires_delta=None
    )

    decoded_token = jwt.decode(token, "test_secret_key", "HS256")

    test_expires = mock_now + timedelta(minutes=15)

    assert decoded_token["sub"] == "1234"
    assert decoded_token["username"] == "test_username"
    assert "exp" in decoded_token
    assert int(decoded_token["exp"]) == int(test_expires.timestamp())


def test_decode_access_token(mocker):
    mocker.patch("app.config.settings.SECRET_KEY", "test_secret_key")
    mocker.patch("app.config.settings.ALGORITHM", "HS256")
    test_datetime_now_expired = datetime.now(timezone.utc) + timedelta(minutes=30)
    
    test_token_data = {
        "sub": "1234",
        "username": "test_username",
        "exp": test_datetime_now_expired
    }

    test_token = jwt.encode(test_token_data, "test_secret_key", "HS256")

    decoded_token = decode_access_token(test_token)

    assert isinstance(decoded_token, TokenData) is True

    assert decoded_token.user_id == "1234"
    assert decoded_token.username == "test_username"
    assert int(decoded_token.expires) == int(test_datetime_now_expired.timestamp())


def test_decode_access_token_expired_token(mocker, capsys):
    mocker.patch("app.config.settings.SECRET_KEY", "test_secret_key")
    mocker.patch("app.config.settings.ALGORITHM", "HS256")
    test_datetime_now_expired = datetime.now(timezone.utc)
    
    test_token_data = {
        "sub": "1234",
        "username": "test_username",
        "exp": test_datetime_now_expired
    }

    test_token = jwt.encode(test_token_data, "test_secret_key", "HS256")

    time.sleep(1)  # ensure second passes and now token is expired

    with pytest.raises(HTTPException) as exec_info:
        decode_access_token(test_token)

    assert "Token error..." in capsys.readouterr().out
    
    assert exec_info.value.status_code == 401
    assert exec_info.value.detail == "Could not validate credentials"
    assert exec_info.value.headers == {"WWW-Authenticate": "Bearer"}


def test_decode_access_token_invalid_token_data(mocker, caplog):
    mocker.patch("app.config.settings.SECRET_KEY", "test_secret_key")
    mocker.patch("app.config.settings.ALGORITHM", "HS256")
    test_datetime_now_expired = datetime.now(timezone.utc) + timedelta(minutes=30)
    
    test_token_data = {
        "sub": "1234",
        "fake_type": "random",
        "exp": test_datetime_now_expired
    }

    test_token = jwt.encode(test_token_data, "test_secret_key", "HS256")

    with pytest.raises(HTTPException) as exec_info:
        decode_access_token(test_token)
    
    assert exec_info.value.status_code == 401
    assert exec_info.value.detail == "Could not validate credentials"
    assert exec_info.value.headers == {"WWW-Authenticate": "Bearer"}


def test_get_current_user(mocker):
    test_token_data = TokenData(
        user_id="1234",
        username="test_username",
        expires=123456789
    )

    test_user = User(
        id="1234",
        username="usernameTest",
        first_name="John",
        last_name="Doe",
        email="testemail@gmail.com",
        telephone="123-312-5543",
        hashed_password="super_strong_password",
        profile_pic="default.png"
    )

    mocker.patch("app.core.security.decode_access_token", return_value=test_token_data)
    mocker.patch("app.core.security.get_user", return_value=test_user)

    returned_user = get_current_user(
        "fake_token_string"
    )

    assert returned_user.id == test_user.id
    assert returned_user.username == test_user.username
    assert returned_user.first_name == test_user.first_name
    assert returned_user.last_name == test_user.last_name
    assert returned_user.email == test_user.email
    assert returned_user.telephone == test_user.telephone
    assert returned_user.hashed_password == test_user.hashed_password
    assert returned_user.profile_pic == test_user.profile_pic


def test_decode_access_token_invalid_token_data(mocker, caplog):
    mocker.patch("app.config.settings.SECRET_KEY", "test_secret_key")
    mocker.patch("app.config.settings.ALGORITHM", "HS256")
    test_datetime_now_expired = datetime.now(timezone.utc) + timedelta(minutes=30)
    
    test_token_data = {
        "sub": "1234",
        "fake_type": "random",
        "exp": test_datetime_now_expired
    }

    test_token = jwt.encode(test_token_data, "test_secret_key", "HS256")

    with pytest.raises(HTTPException) as exec_info:
        decode_access_token(test_token)
    
    assert exec_info.value.status_code == 401
    assert exec_info.value.detail == "Could not validate credentials"
    assert exec_info.value.headers == {"WWW-Authenticate": "Bearer"}


def test_get_current_user_no_user_found(mocker):
    test_token_data = TokenData(
        user_id="1234",
        username="test_username",
        expires=123456789
    )

    test_user = None

    mocker.patch("app.core.security.decode_access_token", return_value=test_token_data)
    mocker.patch("app.core.security.get_user", return_value=test_user)

    with pytest.raises(HTTPException) as exec_job:
        get_current_user("fake_token_string")
    
    assert exec_job.value.status_code == 401
    assert exec_job.value.detail == "User not found."


def test_authenticate_user(mocker):
    mock_user = User(
        id="1234",
        username="usernameTest",
        first_name="John",
        last_name="Doe",
        email="testemail@gmail.com",
        telephone="123-312-5543",
        hashed_password="super_strong_password",
        profile_pic="default.png"
    )

    # Mocking the query chain
    mock_query = mocker.MagicMock()
    mock_filter = mocker.MagicMock()

    mock_query.filter.return_value = mock_filter
    mock_filter.first.return_value = mock_user

    # Mock the database session
    mock_db = mocker.MagicMock()
    mock_db.query.return_value = mock_query

    mocker.patch("app.core.security.verify_password", return_value=True)

    returned_user = authenticate_user(mock_db, "test_username", "password")

    assert returned_user == mock_user


def test_authenticate_user_cannot_find_user(mocker):
    mock_user = None

    # Mocking the query chain
    mock_query = mocker.MagicMock()
    mock_filter = mocker.MagicMock()

    mock_query.filter.return_value = mock_filter
    mock_filter.first.return_value = mock_user

    # Mock the database session
    mock_db = mocker.MagicMock()
    mock_db.query.return_value = mock_query

    mocker.patch("app.core.security.verify_password", return_value=True)
    
    with pytest.raises(HTTPException) as exec_job:
        authenticate_user(mock_db, "test_username", "password")

    assert exec_job.value.status_code == 401
    assert exec_job.value.detail == "Invalid credentials."


def test_authenticate_user_invalid_password(mocker):
    mock_user = User(
        id="1234",
        username="usernameTest",
        first_name="John",
        last_name="Doe",
        email="testemail@gmail.com",
        telephone="123-312-5543",
        hashed_password="super_strong_password",
        profile_pic="default.png"
    )

    # Mocking the query chain
    mock_query = mocker.MagicMock()
    mock_filter = mocker.MagicMock()

    mock_query.filter.return_value = mock_filter
    mock_filter.first.return_value = mock_user

    # Mock the database session
    mock_db = mocker.MagicMock()
    mock_db.query.return_value = mock_query

    mocker.patch("app.core.security.verify_password", return_value=False)
    
    with pytest.raises(HTTPException) as exec_job:
        authenticate_user(mock_db, "test_username", "password")

    assert exec_job.value.status_code == 401
    assert exec_job.value.detail == "Invalid credentials."


def test_login_user(mocker):
    mock_user = User(
        id="1234",
        username="usernameTest",
        first_name="John",
        last_name="Doe",
        email="testemail@gmail.com",
        telephone="123-312-5543",
        hashed_password="super_strong_password",
        profile_pic="default.png"
    )

    mocker.patch("app.core.security.authenticate_user", return_value=mock_user)
    mocker.patch("app.core.security.create_access_token", return_value="test_access_token")
    mocker.patch("app.config.settings.ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    mock_db = mocker.MagicMock()

    token = login_user(mock_db, "test_username", "password")
    
    assert "access_token" in token
    assert "token_type" in token
    assert token["access_token"] == "test_access_token"
    assert token["token_type"] == "bearer"
