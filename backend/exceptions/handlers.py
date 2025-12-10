from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import IntegrityError, DataError

from .app_exception import AppException
from .exception_handler import (
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    database_exception_handler,
    generic_exception_handler,
)


EXCEPTION_HANDLERS = [
    (AppException, app_exception_handler),
    (StarletteHTTPException, http_exception_handler),
    (RequestValidationError, validation_exception_handler),
    (IntegrityError, database_exception_handler),
    (DataError, database_exception_handler),
    (Exception, generic_exception_handler),
]
