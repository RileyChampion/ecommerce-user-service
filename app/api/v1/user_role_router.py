from fastapi import APIRouter, Depends
from app.models.users import User
from app.core.security import (
    get_current_user
)

router = APIRouter()


@router.patch("/assign")
async def assign_user_role(
    current_user: User = Depends(get_current_user)
):
    return {}