from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordRequestForm,
)
from exceptions import AppException
from core.config import get_settings
from core.deps import get_user_manager
from core.users import current_user
from jwt.exceptions import InvalidTokenError
from core.auth import get_refresh_jwt_strategy, get_jwt_strategy
from domains.users.schemas import UserResponse, UserCreate, UserUpdate
from core.schemas.auth import (
    TokenResponse,
    ForgotPasswordRequest,
    RequestVerifyTokenRequest,
    VerifyEmailRequest,
    ResetPasswordRequest,
)
from core.schemas.base import DataResponse
from domains.users.model import User
from core.permissions import get_user_permissions

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix="/auth", tags=["Authentication"], dependencies=[Depends(http_bearer)]
)


@router.post("/register", response_model=DataResponse[UserResponse])
async def register(user_create: UserCreate, user_manager=Depends(get_user_manager)):
    user = await user_manager.create(user_create, safe=True, request=None)
    return DataResponse(data=user)


@router.get("/users/me", response_model=DataResponse[UserResponse])
async def get_current_user_wrapped(user: User = Depends(current_user)):
    user.permissions = get_user_permissions(user)

    return DataResponse(data=user)


@router.get("/users/{id}", response_model=DataResponse[UserResponse])
async def get_user_wrapped(id: int, user_manager=Depends(get_user_manager)):
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
    payload: ResetPasswordRequest,
    user_manager=Depends(get_user_manager),
):
    try:
        await user_manager.reset_password(
            payload.token.get_secret_value(),
            payload.password.get_secret_value(),
        )
        return DataResponse(data={"detail": "Password successfully reset"})
    except Exception:
        raise AppException("Invalid or expired token", status_code=400)


@router.post("/forgot-password", response_model=DataResponse[dict])
async def forgot_password(
    payload: ForgotPasswordRequest,
    request: Request,
    user_manager=Depends(get_user_manager),
):
    user = await user_manager.get_by_email(payload.email)
    if user:
        await user_manager.forgot_password(user, request)
    return DataResponse(data={"detail": "Password reset email sent"})


@router.post("/request-verify-token", response_model=DataResponse[dict])
async def request_verify_token(
    payload: RequestVerifyTokenRequest,
    request: Request,
    user_manager=Depends(get_user_manager),
):
    user = await user_manager.get_by_email(payload.email)
    if user and not user.is_verified:
        await user_manager.request_verify(user, request)
    return DataResponse(data={"detail": "Verification email sent"})


@router.post("/verify", response_model=DataResponse[UserResponse])
async def verify(
    payload: VerifyEmailRequest,
    user_manager=Depends(get_user_manager),
):
    try:
        user = await user_manager.verify(payload.token.get_secret_value())
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
    if not user:
        raise AppException(
            "Incorrect credentials", status_code=401, error_type="invalid_credentials"
        )
    elif not user.is_verified:
        raise AppException("Inactive user", status_code=403, error_type="inactive_user")

    settings = get_settings()

    access_token = await get_jwt_strategy().write_token(user)
    refresh_token = await get_refresh_jwt_strategy().write_token(user)

    _set_refresh_cookie(response, refresh_token, settings)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )


@router.post("/logout")
async def logout(response: Response):
    _clear_refresh_cookie(response, get_settings())

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

    settings = get_settings()

    access_strategy = get_jwt_strategy()
    access_token = await access_strategy.write_token(user)
    new_refresh_token = await refresh_strategy.write_token(user)

    _set_refresh_cookie(response, new_refresh_token, settings)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )


def _set_refresh_cookie(response: Response, token: str, settings) -> None:
    """Set the refresh token cookie using config-driven settings."""
    cookie_config = settings.auth.cookie
    response.set_cookie(
        key="refresh_token",
        value=token,
        httponly=True,
        secure=cookie_config.secure,
        samesite=cookie_config.samesite,
        domain=cookie_config.domain,
        max_age=settings.auth.refresh_token_expire_days * 24 * 60 * 60,
    )


def _clear_refresh_cookie(response: Response, settings) -> None:
    """Delete the refresh token cookie using the same config as when it was set."""
    cookie_config = settings.auth.cookie
    response.delete_cookie(
        key="refresh_token",
        secure=cookie_config.secure,
        httponly=True,
        samesite=cookie_config.samesite,
        domain=cookie_config.domain,
    )
