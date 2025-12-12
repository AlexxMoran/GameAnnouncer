import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError, DataError
import re

from .app_exception import AppException

logger = logging.getLogger(__name__)


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

    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle Pydantic validation errors."""
    logger.warning(
        f"ValidationError on {request.method} {request.url.path}: {exc.errors()}"
    )

    # Format errors into a single readable string
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
    """Handle database exceptions with meaningful error messages."""
    logger.error(f"Database error on {request.method} {request.url.path}: {exc}")

    if isinstance(exc, IntegrityError):
        orig = getattr(exc, "orig", None)
        error_detail = str(orig) if orig else str(exc)
        error_detail_lower = error_detail.lower()

        # Unique constraint violation
        if (
            "unique constraint" in error_detail_lower
            or "duplicate key" in error_detail_lower
        ):
            field = None
            match = re.search(r'"(\w+)_(\w+)_key"', error_detail)
            if match:
                field = match.group(2)

            message = (
                f"{field.capitalize()} already exists"
                if field
                else "Value already exists"
            )

            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT, content={"detail": message}
            )

        # Foreign key violation
        elif "foreign key" in error_detail_lower:
            match = re.search(
                r'Key \((\w+)\)=\(.*?\) is not present in table "(\w+)"', error_detail
            )
            table = match.group(2) if match else "related entity"

            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": f"Referenced {table} does not exist"},
            )

        # Not null violation
        elif "not-null" in error_detail_lower or "null value" in error_detail_lower:
            match = re.search(r'column "(\w+)"', error_detail)
            field = match.group(1) if match else "field"

            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": f"{field.capitalize()} is required"},
            )

        # Check constraint violation
        elif "check constraint" in error_detail_lower:
            match = re.search(r'constraint "(\w+)"', error_detail)
            constraint = match.group(1) if match else "constraint"

            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": f"Value violates constraint: {constraint}"},
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
