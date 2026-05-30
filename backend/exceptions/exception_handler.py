import logging
from typing import Any
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

_HTTP_MESSAGE_KEYS: dict[int, str] = {
    status.HTTP_401_UNAUTHORIZED: "unauthorized",
    status.HTTP_403_FORBIDDEN: "forbidden",
    status.HTTP_404_NOT_FOUND: "not_found",
}

ERROR_PATTERNS = [
    {
        "pattern": r"duplicate key value violates unique constraint",
        "regex": r"Key\s*\(([^)]+)\)=\(([^)]+)\)",
        "status": status.HTTP_409_CONFLICT,
        "message": lambda key, _: f"{key}: Value already exists",
        "message_key": "db.duplicate_key",
    },
    {
        "pattern": r"foreign key",
        "regex": r'Key \(([^)]+)\)=\([^)]+\) is not present in table "([^"]+)"',
        "status": status.HTTP_400_BAD_REQUEST,
        "message": lambda _, table: f"{table}: Referenced entity does not exist",
        "message_key": "db.foreign_key",
    },
    {
        "patterns": ("not-null", "null value"),
        "regex": r'column "([^"]+)"',
        "status": status.HTTP_400_BAD_REQUEST,
        "message": lambda field, _: f"{field}: Field is required",
        "message_key": "db.not_null",
    },
    {
        "pattern": r"check constraint",
        "regex": r'constraint "([^"]+)"',
        "status": status.HTTP_400_BAD_REQUEST,
        "message": lambda constraint, _: f"{constraint}: Value violates constraint",
        "message_key": "db.check_constraint",
    },
]


def _extract_regex(pattern: str, text: str, group: int = 1):
    match = re.search(pattern, text)

    return match.group(group) if match else None


def _sanitize_validation_errors(errors: list[dict]) -> list[dict]:
    """Drop raw input values from validation errors before logging."""
    sanitized_errors: list[dict] = []

    for error in errors:
        sanitized_error = {key: value for key, value in error.items() if key != "input"}
        sanitized_errors.append(sanitized_error)

    return sanitized_errors


def _matches_database_error(pattern_def: dict[str, Any], error_detail: str) -> bool:
    patterns = pattern_def.get("patterns")
    if patterns:
        return any(pattern in error_detail for pattern in patterns)

    pattern = pattern_def.get("pattern")
    return bool(pattern and pattern in error_detail)


def _json_safe_params(params: dict[str, Any] | None) -> dict[str, Any]:
    """Keep localization params JSON-safe and compact."""
    if not params:
        return {}

    safe_params: dict[str, Any] = {}
    for key, value in params.items():
        if isinstance(value, str | int | float | bool) or value is None:
            safe_params[key] = value
        else:
            safe_params[key] = str(value)
    return safe_params


def _validation_message_key(error_type: str | None) -> str:
    if not error_type:
        return "validation.unknown"
    return f"validation.{error_type.replace('.', '_')}"


def _format_validation_error(error: dict) -> dict[str, Any]:
    field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
    message = error["msg"]
    params = _json_safe_params(error.get("ctx"))
    if field:
        params.setdefault("field", field)

    return {
        "field": field,
        "message": message,
        "message_key": _validation_message_key(error.get("type")),
        "params": params,
    }


def _format_database_error(
    message_key: str,
    field: str | None = None,
    **params: Any,
) -> dict[str, Any]:
    safe_params = _json_safe_params(params)
    if field:
        safe_params.setdefault("field", field)

    return {
        "field": field,
        "message_key": message_key,
        "params": safe_params,
    }


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle custom AppException."""
    logger.error(f"AppException on {request.method} {request.url.path}: {exc.message}")

    content = {"detail": exc.message}
    if exc.error_type:
        content["error_type"] = exc.error_type

    if exc.error:
        content["error"] = exc.error

    if exc.message_key:
        content["message_key"] = exc.message_key

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
                jwt.decode(
                    token, options={"verify_signature": False, "verify_exp": True}
                )
                content["error_type"] = "invalid_token"
            except ExpiredSignatureError:
                content["error_type"] = "token_expired"
            except Exception:
                content["error_type"] = "invalid_token"

    message_key = _HTTP_MESSAGE_KEYS.get(exc.status_code)
    if message_key:
        content["message_key"] = message_key

    return JSONResponse(status_code=exc.status_code, content=content)


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle Pydantic validation errors."""
    sanitized_errors = _sanitize_validation_errors(exc.errors())
    logger.warning(
        f"ValidationError on {request.method} {request.url.path}: {sanitized_errors}"
    )

    errors = [_format_validation_error(error) for error in sanitized_errors]
    error_messages = [
        f"{error['field']}: {error['message']}" if error["field"] else error["message"]
        for error in errors
    ]

    detail = "; ".join(error_messages)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "detail": detail,
            "message_key": "validation_error",
            "errors": errors,
        },
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
            if _matches_database_error(pattern_def, error_detail_lower):
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
                pattern_message_key = pattern_def.get(
                    "message_key", "db.integrity_violation"
                )
                params = {}
                if value and pattern_message_key == "db.foreign_key":
                    params["table"] = value
                if key and pattern_message_key == "db.check_constraint":
                    params["constraint"] = key
                return JSONResponse(
                    status_code=status_code,
                    content={
                        "detail": message,
                        "message_key": pattern_message_key,
                        "errors": [
                            _format_database_error(
                                pattern_message_key,
                                field=key,
                                **params,
                            )
                        ],
                    },
                )

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": "Data integrity violation",
                "message_key": "db.integrity_violation",
                "errors": [
                    _format_database_error("db.integrity_violation"),
                ],
            },
        )

    elif isinstance(exc, DataError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": "Invalid data format",
                "message_key": "db.invalid_data_format",
                "errors": [
                    _format_database_error("db.invalid_data_format"),
                ],
            },
        )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Database error occurred", "message_key": "db.error"},
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle any unhandled exceptions."""
    logger.exception(
        f"Unhandled exception on {request.method} {request.url.path}: {exc}"
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred", "message_key": "server_error"},
    )
