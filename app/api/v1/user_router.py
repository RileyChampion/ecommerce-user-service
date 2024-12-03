from fastapi import APIRouter, Path, Query, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Annotated, Literal, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.users import User

from app.core.dependencies import get_db
from app.core.security import (
    verify_password,
    get_current_user,
    is_admin
)
from app.crud.user import (
    get_all_users,
    get_user,
    create_user,
    delete_user,
    update_user_info
)
from app.schemas.filters import UserFilter
from app.schemas.user import UserResponse, UserResponseWithRelaltionships, UserCreate, UserInfoUpdate
from app.schemas.user_role import UserRoleResponse
from app.schemas.user_preference import UserPreferenceResponse
from app.schemas.user_address import UserAddressResponse
from app.schemas.requests import LoginRequest, LogoutRequest

router = APIRouter()


@router.get("/users", status_code=status.HTTP_200_OK, response_model=List[UserResponse])
async def get_users(
    filter_query: Annotated[UserFilter, Query()],
    current_user: User = Depends(get_current_user),
    db_session: Session = Depends(get_db)
):
    if current_user:
        users: List[User] = get_all_users(db_session, filter_query)
        
        user_output = [
            UserResponse(
                id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                telephone=user.telephone,
                profile_pic=user.profile_pic
            ) for user in users
        ]
        
        return user_output


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_id(
    user_id: Annotated[int, Path(title="The ID of a user to get")],
    current_user: User = Depends(get_current_user),
    db_session: Session = Depends(get_db)
):
    if current_user:
        user: User = get_user(db_session, user_id)
        
        user_output = UserResponseWithRelaltionships(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            telephone=user.telephone,
            profile_pic=user.profile_pic,
            addresses=[
                UserAddressResponse(
                    address_line1=address.address_line1,
                    address_line2=address.address_line2,
                    city=address.city,
                    state=address.state,
                    zip_code=address.zip_code,
                    country_code=address.country_code,
                    is_primary=address.is_primary
                ) for address in user.addresses
            ],
            roles=[
                UserRoleResponse(
                    role_name=role.role_name
                ) for role in user.roles
            ],
            preferences=[
                UserPreferenceResponse(
                    preference_type=preference.preference_type,
                    preference_value=preference.preference_value
                ) for preference in user.preferences
            ]
        )

        return user_output


# @router.get("/search", status_code=200)
# async def get_user_username(
#     username: Annotated[str, Query()],
#     current_user: User = Depends(get_current_user),
#     db_session: Session = Depends(get_db)
# ):
#     if current_user:
#         user: User = get_user_by_username(db_session, username)
        
#         user_output = UserResponseWithRelaltionships(
#             id=user.id,
#             username=user.username,
#             first_name=user.first_name,
#             last_name=user.last_name,
#             email=user.email,
#             telephone=user.telephone,
#             profile_pic=user.profile_pic,
#             addresses=[
#                 UserAddressResponse(
#                     address_line1=address.address_line1,
#                     address_line2=address.address_line2,
#                     city=address.city,
#                     state=address.state,
#                     zip_code=address.zip_code,
#                     country_code=address.country_code,
#                     is_primary=address.is_primary
#                 ) for address in user.addresses
#             ],
#             roles=[
#                 UserRoleResponse(
#                     role_name=role.role_name
#                 ) for role in user.roles
#             ],
#             preferences=[
#                 UserPreferenceResponse(
#                     preference_type=preference.preference_type,
#                     preference_value=preference.preference_value
#                 ) for preference in user.preferences
#             ]
#         )

#         return user_output


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_new_user(
    user_create_payload: UserCreate,
    current_user: User = Depends(get_current_user),
    db_session: Session = Depends(get_db)
):
    #  TODO: NEED TO CREATE DEFAULT ROLE AND DEFAULT PREFERENCES
    try:
        if current_user:
            created_user: User = create_user(db_session, user_create_payload)

            created_user_response = UserResponse(
                id=created_user.id,
                username=created_user.username,
                first_name=created_user.first_name,
                last_name=created_user.last_name,
                email=created_user.email,
                telephone=created_user.telephone,
                profile_pic=created_user.profile_pic
            )

            db_session.commit()
            return created_user_response
    except IntegrityError as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username already taken.',
            headers={"WWW-Authenticate": "Bearer"}
        )


@router.delete("/delete/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user_from_service(
    user_id: Annotated[int, Path(title="The ID of a user to get")],
    current_user: User = Depends(get_current_user),
    db_session: Session = Depends(get_db)
):
    try:
        if is_admin(current_user) or current_user.id == user_id:
            delete_user(db_session, user_id)
            db_session.commit()

            return {"messages": "Deleted user."}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized request.",
                headers={"WWW-Authenticate": "Bearer"}
            )
    except ValueError as e:
        db_session.rollback()

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unable to delete entered user."
        )


@router.patch("/update/{user_id}")
async def update_user(
    updated_user_info: UserInfoUpdate,
    user_id: Annotated[int, Path(title="The ID of a user to get")],
    current_user: User = Depends(get_current_user),
    db_session: Session = Depends(get_db)
):
    # TODO:  Update user information
    try:
        if is_admin(current_user) or current_user.id == user_id:
            update_user_info(db_session, user_id, updated_user_info)
            
            return {"messages": "Updated user."}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized request.",
                headers={"WWW-Authenticate": "Bearer"}
            )
    except ValueError as e:
        db_session.rollback()

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unable to update entered user."
        )


@router.post("/login")
async def login(
    login_credentials: LoginRequest,
    current_user: User = Depends(get_current_user),
    db_session: Session = Depends(get_db)
):
    # TODO:  Login Route
    if (
        current_user
        and current_user.username == login_credentials.username
        and verify_password(login_credentials.password, current_user.hashed_password)
    ):
        current_user.is_active = True
        db_session.commit()

        return {"message": "Successfully logged in."}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password.",
        )
        

@router.post("/logout")
async def logout(
    logging_out_user: LogoutRequest,
    current_user: User = Depends(get_current_user),
    db_session: Session = Depends(get_db)
):
    if current_user.id == logging_out_user.user_id:
        current_user.is_active = False
        db_session.commit()

        return {"message": "Successfully logged out."}
