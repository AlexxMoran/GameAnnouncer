from fastapi_users.authentication import (
    BearerTransport,
    JWTStrategy,
    AuthenticationBackend,
)
from core.config import get_settings


bearer_transport = BearerTransport(tokenUrl="/api/auth/login")
refresh_bearer_transport = BearerTransport(tokenUrl="/api/auth/jwt/refresh")


def get_jwt_strategy() -> JWTStrategy:
    settings = get_settings()

    return JWTStrategy(
        secret=settings.auth.secret_key,
        lifetime_seconds=settings.auth.access_token_expire_minutes * 60,
        token_audience=["gameannouncer:auth"],
        algorithm=settings.auth.algorithm,
    )


def get_refresh_jwt_strategy() -> JWTStrategy:
    settings = get_settings()

    return JWTStrategy(
        secret=settings.auth.refresh_secret_key,
        lifetime_seconds=settings.auth.refresh_token_expire_days * 24 * 60 * 60,
        token_audience=["gameannouncer:refresh"],
        algorithm=settings.auth.algorithm,
    )


def get_auth_backend() -> AuthenticationBackend:
    return AuthenticationBackend(
        name="jwt",
        transport=bearer_transport,
        get_strategy=get_jwt_strategy,
    )


def get_refresh_auth_backend() -> AuthenticationBackend:
    return AuthenticationBackend(
        name="jwt_refresh",
        transport=refresh_bearer_transport,
        get_strategy=get_refresh_jwt_strategy,
    )
