from fastapi import HTTPException, status


class BasePolicy:
    def __init__(self, user, record=None):
        self.user = user
        self.record = record

    def deny(self):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action.",
        )

    @property
    def is_admin(self):
        return getattr(self.user, "is_superuser", False)
