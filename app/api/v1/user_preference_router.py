from fastapi import APIRouter, Path, Depends
from typing import Annotated
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


class PreferenceFilter:
    pass


@router.get("/all", tags=["Preferences"])
async def get_all_user_preferences(
    current_user: User = Depends(get_current_user)
):
    return []


@router.get("{user_id}/get", tags=["Preferences"])
async def get_user_preferences(
    user_id: Annotated[int, Path(title="The ID of a user to get")],
    current_user: User = Depends(get_current_user)
):
    return {user_id}


@router.patch("/{user_id}/set", tags=["Preferences"])
async def set_user_preference(
    user_id: Annotated[int, Path(title="The ID of a user to get")],
    current_user: User = Depends(get_current_user)
):
    return {}
