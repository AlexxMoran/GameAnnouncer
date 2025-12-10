from fastapi import status
from exceptions import AppException


class BasePolicy:
    def __init__(self, user, record=None):
        self.user = user
        self.record = record

    def deny(self):
        raise AppException(
            "You do not have permission to perform this action",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    @property
    def is_admin(self):
        return getattr(self.user, "is_superuser", False)
