from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.core.security import (
    Token,
    login_user
)

router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    login_request: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    logged_user = login_user(
        db=db,
        username=login_request.username,
        password=login_request.password
    )
    return Token(
        access_token=logged_user["access_token"],
        token_type=logged_user["token_type"]
    )


@router.post("/login")
async def login():
    pass


@router.post("/logout")
async def logout():
    pass
