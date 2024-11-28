from fastapi import APIRouter, Path, Query, Depends
from pydantic import BaseModel, Field
from typing import Annotated, Literal
from app.models.users import User
from app.core.security import (
    get_current_user
)

# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.schemas.user import UserCreate, UserOut
# from app.crud.user import create_user
# from app.core.dependencies import get_db

router = APIRouter()


class UserFilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, gt=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"


@router.get("/users", status_code=200)
async def get_users(
    filter_query: Annotated[UserFilterParams, Query()],
    current_user: User = Depends(get_current_user)
):
    return []


@router.get("/{user_id}", status_code=200)
async def get_user_id(
    user_id: Annotated[int, Path(title="The ID of a user to get")],
    current_user: User = Depends(get_current_user)
):
    return {}


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
    return {}


@router.delete("/delete/{user_id}")
async def delete_user(
    user_id: Annotated[int, Path(title="The ID of a user to get")],
    current_user: User = Depends(get_current_user)
):
    return {}


@router.patch("/update/{user_id}")
async def update_user(
    user_id: Annotated[int, Path(title="The ID of a user to get")],
    current_user: User = Depends(get_current_user)
):
    return {}


@router.post("/login")
async def login(current_user: User = Depends(get_current_user)):
    return {}


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user)
):
    pass
