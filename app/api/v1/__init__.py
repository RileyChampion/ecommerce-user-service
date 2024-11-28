from fastapi import APIRouter
from app.api.v1.user_router import router as user_router
from app.api.v1.user_role_router import router as user_role_router
from app.api.v1.user_preference_router import router as user_preference_router

api_router = APIRouter()
api_router.include_router(user_router, prefix="/user", tags=["Users"])
api_router.include_router(
    user_role_router,
    prefix="/user/role",
    tags=["Roles"]
)
api_router.include_router(
    user_preference_router,
    prefix="/user/preference",
    tags=["Preferences"]
)
