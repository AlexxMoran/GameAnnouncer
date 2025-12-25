import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError, DataError
import re

import jwt
from jwt import ExpiredSignatureError

from .app_exception import AppException

logger = logging.getLogger(__name__)

ERROR_PATTERNS = [
    {
        "pattern": r"duplicate key value violates unique constraint",
        "regex": r"Key\s*\(([^)]+)\)=\(([^)]+)\)",
        "status": status.HTTP_409_CONFLICT,
        "message": lambda key, _: f"{key}: Value already exists",
    },
    {
        "pattern": r"foreign key",
        "regex": r'Key \(([^)]+)\)=\([^)]+\) is not present in table "([^"]+)"',
        "status": status.HTTP_400_BAD_REQUEST,
        "message": lambda _, table: f"{table}: Referenced entity does not exist",
    },
    {
        "pattern": r"not-null|null value",
        "regex": r'column "([^"]+)"',
        "status": status.HTTP_400_BAD_REQUEST,
        "message": lambda field, _: f"{field}: Field is required",
    },
    {
        "pattern": r"check constraint",
        "regex": r'constraint "([^"]+)"',
        "status": status.HTTP_400_BAD_REQUEST,
        "message": lambda constraint, _: f"{constraint}: Value violates constraint",
    },
]


def _extract_regex(pattern: str, text: str, group: int = 1):
    match = re.search(pattern, text)

    return match.group(group) if match else None


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle custom AppException."""
    logger.error(f"AppException on {request.method} {request.url.path}: {exc.message}")

    content = {"detail": exc.message}
    if exc.error_type:
        content["error_type"] = exc.error_type

    if exc.error:
        content["error"] = exc.error

    return JSONResponse(status_code=exc.status_code, content=content)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle standard HTTPException."""
    logger.warning(
        f"HTTPException on {request.method} {request.url.path}: {exc.detail}"
    )

    content = {"detail": exc.detail}

    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        authorization = request.headers.get("authorization", "")

        if not authorization or not authorization.startswith("Bearer "):
            content["error_type"] = "missing_token"
        else:
            token = authorization.replace("Bearer ", "")
            try:
                jwt.decode(token, options={"verify_signature": False})
                content["error_type"] = "invalid_token"
            except ExpiredSignatureError:
                content["error_type"] = "token_expired"
            except Exception:
                content["error_type"] = "invalid_token"

    return JSONResponse(status_code=exc.status_code, content=content)


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle Pydantic validation errors."""
    logger.warning(
        f"ValidationError on {request.method} {request.url.path}: {exc.errors()}"
    )

    error_messages = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
        message = error["msg"]
        error_messages.append(f"{field}: {message}")

    detail = "; ".join(error_messages)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": detail}
    )


async def database_exception_handler(
    request: Request, exc: IntegrityError | DataError
) -> JSONResponse:
    """Generic database exception handler for SQLAlchemy / asyncpg."""
    logger.error(f"Database error on {request.method} {request.url.path}: {exc}")

    orig = getattr(exc, "orig", None)
    error_detail = str(orig) if orig else str(exc)
    error_detail_lower = error_detail.lower()

    if isinstance(exc, IntegrityError):
        for pattern_def in ERROR_PATTERNS:
            if pattern_def["pattern"] in error_detail_lower:
                regex = pattern_def.get("regex")
                status_code = pattern_def.get("status", status.HTTP_400_BAD_REQUEST)
                message_func = pattern_def.get("message")

                key = _extract_regex(regex, error_detail) if regex else None
                value = None

                match = re.search(regex, error_detail) if regex else None
                if match and len(match.groups()) > 1:
                    value = match.group(2)

                message = (
                    message_func(key, value)
                    if message_func
                    else "Data integrity violation"
                )
                return JSONResponse(
                    status_code=status_code, content={"detail": message}
                )

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Data integrity violation"},
        )

    elif isinstance(exc, DataError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Invalid data format"},
        )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Database error occurred"},
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle any unhandled exceptions."""
    logger.exception(
        f"Unhandled exception on {request.method} {request.url.path}: {exc}"
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred"},
    )
