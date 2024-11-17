from fastapi import APIRouter, Path, Query
from pydantic import BaseModel, Field
from typing import Annotated, Literal

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


@router.get("/users", tags=["users"], status_code=200)
async def get_users(
    filter_query: Annotated[UserFilterParams, Query()]
):
    return []


@router.get("/{user_id}", tags=["users"], status_code=200)
async def get_user_id(
    user_id: Annotated[int, Path(title="The ID of a user to get")]
):
    return {}


@router.get("/{username}", tags=["users"], status_code=200)
async def get_user_username(
    username: Annotated[str, Path(title="The USERNAME of a user to get")]
):
    return {}


@router.post("/create", tags=["users"], status_code=201)
async def create_user():
    return {}


@router.delete("/delete/{user_id}", tags=["users"])
async def delete_user(
    user_id: Annotated[int, Path(title="The ID of a user to get")]
):
    return {}


@router.patch("/update/{user_id}", tags=["users"])
async def update_user(
    user_id: Annotated[int, Path(title="The ID of a user to get")]
):
    return {}


@router.patch("/assign", tags=["userAssign"])
async def assign_user_role():
    return {}
