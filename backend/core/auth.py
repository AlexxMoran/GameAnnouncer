from fastapi_users.authentication import (
    BearerTransport,
    JWTStrategy,
    AuthenticationBackend,
)
from core.config import get_settings

settings = get_settings()

bearer_transport = BearerTransport(tokenUrl="/api/auth/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.auth.secret_key,
        lifetime_seconds=settings.auth.access_token_expire_minutes * 60,
        token_audience=["gameannouncer:auth"],
        algorithm=settings.auth.algorithm,
    )


refresh_bearer_transport = BearerTransport(tokenUrl="/api/auth/jwt/refresh")


def get_refresh_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.auth.refresh_secret_key,
        lifetime_seconds=settings.auth.refresh_token_expire_days * 24 * 60 * 60,
        token_audience=["gameannouncer:refresh"],
        algorithm=settings.auth.algorithm,
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

refresh_auth_backend = AuthenticationBackend(
    name="jwt_refresh",
    transport=refresh_bearer_transport,
    get_strategy=get_refresh_jwt_strategy,
)
