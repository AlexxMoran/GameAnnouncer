from tasks.broker import get_broker
from core.logger import logger
from mailers.user_mailer import UserMailer

broker = get_broker()


@broker.task
async def send_verification_email_task(email: str, token: str, first_name: str = None):
    """Send verification email via taskiq."""
    logger.info(f"📧 Processing verification email for {email}")

    mailer = UserMailer()
    mail = mailer.verification_email(email, token, first_name)
    result = await mailer.deliver(mail)

    if result:
        logger.info(f"✅ Verification email sent to {email}")
    else:
        logger.error(f"❌ Failed to send verification email to {email}")

    return result


@broker.task
async def send_password_reset_email_task(
    email: str, token: str, first_name: str = None
):
    """Send password reset email via taskiq."""
    logger.info(f"📧 Processing password reset email for {email}")

    mailer = UserMailer()
    mail = mailer.password_reset_email(email, token, first_name)
    result = await mailer.deliver(mail)

    if result:
        logger.info(f"✅ Password reset email sent to {email}")
    else:
        logger.error(f"❌ Failed to send password reset email to {email}")

    return result
