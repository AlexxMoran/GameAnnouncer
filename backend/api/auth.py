from fastapi import APIRouter
from core.users import fastapi_users
from core.auth import auth_backend
from schemas.user import UserResponse, UserCreate, UserUpdate

router = APIRouter(prefix="/auth", tags=["Authentication"])

router.include_router(
    fastapi_users.get_register_router(UserResponse, UserCreate),
)

router.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/jwt")

router.include_router(
    fastapi_users.get_users_router(UserResponse, UserUpdate),
    prefix="/users",
)

router.include_router(
    fastapi_users.get_reset_password_router(),
)

router.include_router(
    fastapi_users.get_verify_router(UserResponse),
)
