from fastapi import APIRouter, Path, Query, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Annotated, Literal, List
from sqlalchemy.orm import Session
from app.models.users import User

from app.core.dependencies import get_db
from app.core.security import (
    get_current_user,
    is_admin
)
from app.crud.user import (
    get_all_users,
    get_user
)
from app.schemas.filters import UserFilter
from app.schemas.user import UserResponse, UserResponseWithRelaltionships
from app.schemas.user_role import UserRoleResponse
from app.schemas.user_preference import UserPreferenceResponse
from app.schemas.user_address import UserAddressResponse

# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.schemas.user import UserCreate, UserOut
# from app.crud.user import create_user
# from app.core.dependencies import get_db

router = APIRouter()


@router.get("/users", status_code=200, response_model=List[UserResponse])
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


@router.get("/{user_id}", status_code=200)
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


@router.get("/{username}", status_code=200)
async def get_user_username(
    username: Annotated[str, Path(title="The USERNAME of a user to get")],
    current_user: User = Depends(get_current_user)
):
    return {}


@router.post("/create", status_code=201)
async def create_user(
    current_user: User = Depends(get_current_user)
):
    if current_user:
        pass


@router.delete("/delete/{user_id}")
async def delete_user(
    user_id: Annotated[int, Path(title="The ID of a user to get")],
    current_user: User = Depends(get_current_user)
):
    if is_admin(current_user) or current_user.id == user_id:
        return {"messages": "Deleted"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized request.",
            headers={"WWW-Authenticate": "Bearer"}
        )


@router.patch("/update/{user_id}")
async def update_user(
    user_id: Annotated[int, Path(title="The ID of a user to get")],
    current_user: User = Depends(get_current_user)
):
    if is_admin(current_user) or current_user.id == user_id:
        return {"messages": "Updated"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized request.",
            headers={"WWW-Authenticate": "Bearer"}
        )


@router.post("/login")
async def login(current_user: User = Depends(get_current_user)):
    return {}


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user)
):
    pass
