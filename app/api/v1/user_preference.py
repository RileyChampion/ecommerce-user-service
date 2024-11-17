from fastapi import APIRouter, Path
from typing import Annotated
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.schemas.user import UserCreate, UserOut
# from app.crud.user import create_user
# from app.core.dependencies import get_db

router = APIRouter()


class PreferenceFilter:
    pass


@router.get("/all", tags=["userPreference"])
async def user_preference_get_all():
    return []


@router.get("{user_id}/get", tags=["userPreference"])
async def user_preference_get(
    user_id: Annotated[int, Path(title="The ID of a user to get")]
):
    return {user_id}


@router.patch("/{user_id}/set", tags=["userPreference"])
async def user_preference_set(
    user_id: Annotated[int, Path(title="The ID of a user to get")]
):
    return {}
