from typing import Any, Optional


class AppException(Exception):
    """
    Custom application exception for standardized error handling.
    """

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_type: Optional[Any] = None,
        error: Optional[Any] = None,
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
