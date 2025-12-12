from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordRequestForm,
)
from pydantic import EmailStr
from exceptions import AppException
from core.deps import get_user_manager
from core.users import current_user
from jwt.exceptions import InvalidTokenError
from core.auth import get_refresh_jwt_strategy, get_jwt_strategy
from schemas.user import UserResponse, UserCreate, UserUpdate
from schemas.auth import TokenResponse
from schemas.base import DataResponse
from models.user import User


http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix="/auth", tags=["Authentication"], dependencies=[Depends(http_bearer)]
)


@router.post("/register", response_model=DataResponse[UserResponse])
async def register(
    user_create: UserCreate = Depends(), user_manager=Depends(get_user_manager)
):
    user = await user_manager.create(user_create, safe=True, request=None)
    return DataResponse(data=user)


@router.get("/users/me", response_model=DataResponse[UserResponse])
async def get_current_user_wrapped(user: User = Depends(current_user)):
    return DataResponse(data=user)


@router.get("/users/{id}", response_model=DataResponse[UserResponse])
async def get_user_wrapped(id: str, user_manager=Depends(get_user_manager)):
    user = await user_manager.get(id)
    if not user:
        raise AppException("User not found", status_code=404)
    return DataResponse(data=user)


@router.patch("/users/me", response_model=DataResponse[UserResponse])
async def update_current_user_wrapped(
    user_update: UserUpdate,
    user: User = Depends(current_user),
    user_manager=Depends(get_user_manager),
):
    user = await user_manager.update(user_update, user, safe=True, request=None)
    return DataResponse(data=user)


@router.post("/reset-password", response_model=DataResponse[dict])
async def reset_password(
    token: str,
    password: str,
    user_manager=Depends(get_user_manager),
):
    try:
        await user_manager.reset_password(token, password)
        return DataResponse(data={"detail": "Password successfully reset"})
    except Exception:
        raise AppException("Invalid or expired token", status_code=400)


@router.post("/forgot-password", response_model=DataResponse[dict])
async def forgot_password(
    email: EmailStr,
    request: Request,
    user_manager=Depends(get_user_manager),
):
    user = await user_manager.get_by_email(email)
    if user:
        await user_manager.forgot_password(user, request)
    return DataResponse(data={"detail": "Password reset email sent"})


@router.post("/request-verify-token", response_model=DataResponse[dict])
async def request_verify_token(
    email: EmailStr,
    request: Request,
    user_manager=Depends(get_user_manager),
):
    user = await user_manager.get_by_email(email)
    if user and not user.is_verified:
        await user_manager.request_verify(user, request)
    return DataResponse(data={"detail": "Verification email sent"})


@router.post("/verify", response_model=DataResponse[UserResponse])
async def verify(
    token: str,
    user_manager=Depends(get_user_manager),
):
    try:
        user = await user_manager.verify(token)
        return DataResponse(data=user)
    except Exception:
        raise AppException("Invalid or expired verification token", status_code=400)


@router.post("/login", response_model=TokenResponse)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_manager=Depends(get_user_manager),
):
    user = await user_manager.authenticate(form_data)
    if not user or not user.is_active:
        raise AppException(
            "Incorrect credentials", status_code=401, error_type="invalid_credentials"
        )

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
async def logout(response: Response):
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
        raise AppException(
            "Refresh token missing", status_code=401, error_type="missing_token"
        )

    refresh_strategy = get_refresh_jwt_strategy()
    try:
        user = await refresh_strategy.read_token(refresh_token, user_manager)
        if not user:
            raise AppException("User not found", status_code=404)
    except InvalidTokenError:
        raise AppException(
            "Invalid refresh token", status_code=401, error_type="invalid_token"
        )

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
