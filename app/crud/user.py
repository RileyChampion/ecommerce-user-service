from typing import List, Union
from sqlalchemy.orm import Session, joinedload, contains_eager
from sqlalchemy import and_
from app.models.users import User
from app.models.user_role_assignments import UserRoleAssignment
from app.models.user_role_assignments import UserRoleAssignment
from app.schemas.user import UserCreate, UserInfoUpdate, UserPasswordUpdate
from app.schemas.filters import UserFilter


def get_all_users(db: Session, filter_params: UserFilter) -> List[User]:
    filters = []
    if filter_params.user_id:
        filters.append(User.id == filter_params.user_id)
    if filter_params.username:
        filters.append(User.username == filter_params.username)
    if filter_params.first_name:
        filters.append(User.first_name == filter_params.first_name)
    if filter_params.last_name:
        filters.append(User.last_name == filter_params.last_name)
    if filter_params.email:
        filters.append(User.email == filter_params.email)
    if filter_params.telephone:
        filters.append(User.telephone == filter_params.telephone)
    
    filters.append(User.is_active == (filter_params.is_active == "true"))

    print(filters)

    limit = filter_params.limit
    offset = filter_params.offset * filter_params.limit
    return db.query(User).filter(and_(*filters))\
        .offset(offset)\
        .limit(limit).all()


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
        hashed_password=user.password,
        profile_pic=user.profile_pic
    )

    db.add(created_user)
    return created_user


def update_user_info(db: Session, user_id: int, update_info: UserInfoUpdate) -> User:
    updating_user = db.query(User).filter(User.id == user_id).first()

    if not updating_user:
        raise ValueError("User not found.")

    updating_user.username = update_info.username
    updating_user.first_name = update_info.first_name
    updating_user.last_name = update_info.last_name
    updating_user.email = update_info.email
    updating_user.telephone = update_info.telephone
    updating_user.profile_pic = update_info.profile_pic
    updating_user.is_active = update_info.is_active

    db.add(updating_user)
    return updating_user


def update_user_password(db: Session, user_id: int, update_password: UserPasswordUpdate) -> User:
    updating_user = db.query(User).filter(User.id == user_id).first()

    if not updating_user:
        raise ValueError("User not found.")

    updating_user.hashed_password = update_password.password

    db.add(updating_user)
    return updating_user


def delete_user(db: Session, user_id: int) -> None:
    deleting_user = db.query(User).filter(User.id == user_id).first()

    if not deleting_user:
        raise ValueError("User not found.")

    db.delete(deleting_user)
