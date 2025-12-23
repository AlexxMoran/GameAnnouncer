import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from core.config import get_settings
from core.logger import logger

settings = get_settings()


class EmailService:
    """Send emails via SMTP asynchronously."""

    @staticmethod
    async def send_email(mail) -> bool:
        """Send email via SMTP asynchronously."""
        try:
            msg = EmailService._build_message(mail)

            async with aiosmtplib.SMTP(
                hostname=settings.email.smtp_host,
                port=settings.email.smtp_port,
            ) as server:
                if settings.email.smtp_user and settings.email.smtp_password:
                    await server.login(
                        settings.email.smtp_user, settings.email.smtp_password
                    )

                await server.send_message(msg)

            logger.info(f"📧 Email sent to {mail.to}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to send email: {e}")
            return False

    @staticmethod
    def _build_message(mail) -> MIMEMultipart:
        """Build MIME message from mail object."""
        msg = MIMEMultipart("alternative")
        msg["Subject"] = mail.subject
        msg["From"] = f"{mail.from_name} <{mail.from_email}>"
        msg["To"] = ", ".join(mail.to)

        if mail.reply_to:
            msg["Reply-To"] = mail.reply_to
        if mail.cc:
            msg["Cc"] = ", ".join(mail.cc)
        if mail.bcc:
            msg["Bcc"] = ", ".join(mail.bcc)

        msg.attach(MIMEText(mail.body, "plain"))

        if mail.html_body:
            msg.attach(MIMEText(mail.html_body, "html"))

        return msg
