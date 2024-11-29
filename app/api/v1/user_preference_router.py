from fastapi import APIRouter, Path, Depends, HTTPException
from typing import Annotated
from app.models.users import User
from app.core.security import (
    get_current_user
)
from app.core.dependencies import get_db
from sqlalchemy.orm import Session
# from app.schemas.user import UserCreate, UserOut


router = APIRouter()


class PreferenceFilter:
    pass


@router.get("/all", tags=["Preferences"])
async def get_all_user_preferences(
    current_user: User = Depends(get_current_user),
    db_session: Session = Depends(get_db)
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
