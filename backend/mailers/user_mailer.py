from mailers.base_mailer import BaseMailer, Mail
from core.config import get_settings


class UserMailer(BaseMailer):
    """Mailer for user-related emails."""

    def __init__(self):
        super().__init__()
        self.settings = get_settings()

    def verification_email(
        self, email: str, token: str, first_name: str = None
    ) -> Mail:
        """Send email verification link."""
        verification_url = (
            f"{self.settings.cors.frontend_host}/verify-email?token={token}"
        )

        return self.mail(
            to=email,
            subject="Verify your email address",
            template="verification_email",
            first_name=first_name,
            verification_url=verification_url,
        )

    def password_reset_email(
        self, email: str, token: str, first_name: str = None
    ) -> Mail:
        """Send password reset link."""
        reset_url = f"{self.settings.cors.frontend_host}/reset-password?token={token}"

        return self.mail(
            to=email,
            subject="Reset your password",
            template="password_reset_email",
            first_name=first_name,
            reset_url=reset_url,
        )
