from core.logger import logger
from typing import Optional
from core.config import get_settings


from fastapi import Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from models.user import User


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    @property
    def reset_password_token_secret(self) -> str:
        return get_settings().auth.reset_password_token_secret

    @property
    def verification_token_secret(self) -> str:
        return get_settings().auth.verification_token_secret

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        logger.info(f"User {user.id} has registered. Generating verification token.")

        await self.request_verify(user, request)

        logger.info(f"Verification email queued for user {user.id}.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.info(f"User {user.id} has forgot their password. Queueing reset email.")
        from tasks import send_password_reset_email_task

        await send_password_reset_email_task.kiq(
            email=user.email, token=token, first_name=user.first_name
        )

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.info(
            f"Verification requested for user {user.id}. Queueing verification email."
        )
        from tasks import send_verification_email_task

        await send_verification_email_task.kiq(
            email=user.email, token=token, first_name=user.first_name
        )
