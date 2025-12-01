from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordRequestForm,
)
from core.deps import get_user_manager
from core.users import fastapi_users, current_user
from jwt.exceptions import InvalidTokenError
from core.auth import auth_backend, get_refresh_jwt_strategy, get_jwt_strategy
from schemas.user import UserResponse, UserCreate, UserUpdate
from schemas.auth import TokenResponse
from models.user import User


http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix="/auth", tags=["Authentication"], dependencies=[Depends(http_bearer)]
)

router.include_router(
    fastapi_users.get_register_router(UserResponse, UserCreate),
)

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


@router.post("/login")
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_manager=Depends(get_user_manager),
):
    user = await user_manager.authenticate(form_data)
    if not user or not user.is_active:
        raise HTTPException(status_code=400, detail="Incorrect credentials")

    access_token = await get_jwt_strategy().write_token(user)
    refresh_token = await get_refresh_jwt_strategy().write_token(user)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=60 * 60 * 24 * 30,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )


@router.post("/logout")
async def logout(
    response: Response,
    user: User = Depends(current_user),
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    strategy=Depends(auth_backend.get_strategy),
):
    token = credentials.credentials
    await auth_backend.logout(strategy, user, token)
    response.delete_cookie(key="refresh_token")

    return {"detail": "Successfully logged out"}


@router.post("/jwt/refresh", response_model=TokenResponse)
async def refresh_access_token(
    request: Request,
    response: Response,
    user_manager=Depends(get_user_manager),
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

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

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=60 * 60 * 24 * 30,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )
