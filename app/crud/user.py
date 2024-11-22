from typing import List, Union
from sqlalchemy.orm import Session, joinedload
from app.models.users import User
from app.schemas.user import UserCreate, UserInfoUpdate, UserPasswordUpdate


def get_all_users(db: Session) -> List[User]:
    return db.query(User).all()


def get_user(db: Session, user_id: int) -> Union[User, None]:
    return db.query(User).options(
        joinedload(User.addresses),
        joinedload(User.preferences),
        joinedload(User.roles)
    ).filter(User.id == user_id).first()


def create_user(db: Session, user: UserCreate) -> User:
    created_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        telephone=user.telephone,
        password=user.password,
        profile_pic=user.profile_pic
    )

    return created_user


def update_user_info(db: Session, user_id: int, update_info: UserInfoUpdate) -> User:
    user_found = db.query(User).filter(User.id == user_id).first()

    if not user_found:
        raise ValueError("User not found.")

    user_found.username = update_info.username
    user_found.first_name = update_info.first_name
    user_found.last_name = update_info.last_name
    user_found.email = update_info.email
    user_found.telephone = update_info.telephone
    user_found.profile_pic = update_info.profile_pic
    user_found.is_active = update_info.is_active

    return user_found


def update_user_password(db: Session, user_id: int, update_password: UserPasswordUpdate) -> User:
    user_found = db.query(User).filter(User.id == user_id).first()

    if not user_found:
        raise ValueError("User not found.")

    user_found.password = update_password.password

    return user_found


def delete_user(db: Session, user_id: int) -> None:
    found_user = db.query(User).filter(User.id == user_id).first()

    if not found_user:
        raise ValueError("User not found.")

    db.delete(found_user)
