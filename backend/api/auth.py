from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordRequestForm,
)
from core.deps import get_user_manager
from core.users import fastapi_users
from jwt.exceptions import InvalidTokenError
from core.auth import auth_backend, get_refresh_jwt_strategy, get_jwt_strategy
from schemas.user import UserResponse, UserCreate, UserUpdate
from schemas.auth import TokenResponse


http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix="/auth", tags=["Authentication"], dependencies=[Depends(http_bearer)]
)

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


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_manager=Depends(get_user_manager),
):
    user = await user_manager.authenticate(form_data)
    if not user or not user.is_active:
        raise HTTPException(status_code=400, detail="Incorrect credentials")

    access_token = await get_jwt_strategy().write_token(user)
    refresh_token = await get_refresh_jwt_strategy().write_token(user)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/jwt/refresh", response_model=TokenResponse)
async def refresh_access_token(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    user_manager=Depends(get_user_manager),
):
    refresh_token = credentials.credentials

    refresh_strategy = get_refresh_jwt_strategy()
    try:
        user = await refresh_strategy.read_token(refresh_token, user_manager)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_strategy = get_jwt_strategy()
    access_token = await access_strategy.write_token(user)
    new_refresh_token = await refresh_strategy.write_token(user)

    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
    )
