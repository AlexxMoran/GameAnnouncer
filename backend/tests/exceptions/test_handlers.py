from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import IntegrityError, DataError

from exceptions.handlers import EXCEPTION_HANDLERS
from exceptions.app_exception import AppException


def test_exception_handlers_mapping_and_names():
    expected_types = [
        AppException,
        StarletteHTTPException,
        RequestValidationError,
        IntegrityError,
        DataError,
        Exception,
    ]

    types_in_file = [t for t, _ in EXCEPTION_HANDLERS]
    assert types_in_file == expected_types

    handlers = {t: h for t, h in EXCEPTION_HANDLERS}

    assert handlers[AppException].__name__ == "app_exception_handler"
    assert handlers[StarletteHTTPException].__name__ == "http_exception_handler"
    assert handlers[RequestValidationError].__name__ == "validation_exception_handler"
    assert handlers[IntegrityError].__name__ == "database_exception_handler"
    assert handlers[DataError].__name__ == "database_exception_handler"
    assert handlers[Exception].__name__ == "generic_exception_handler"
