from typing import Any


class AppException(Exception):
    """
    Custom application exception for standardized error handling.
    """

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_type: Any | None = None,
        error: Any | None = None,
    ):
        self.status_code = status_code
        self.message = message
        self.error_type = error_type
        self.error = error
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"AppException(status_code={self.status_code}, message='{self.message}')"

    def __repr__(self) -> str:
        return self.__str__()


class ValidationException(AppException):
    """
    Custom exception for validation errors.
    """

    def __init__(self, message: str, error: Any | None = None):
        super().__init__(
            message, status_code=422, error_type="validation_error", error=error
        )
