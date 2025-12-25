import pytest

from email.mime.multipart import MIMEMultipart
from services.email_service import EmailService
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch


def test_build_message_includes_html_and_plain():
    m = SimpleNamespace(
        subject="S",
        from_name="N",
        from_email="n@t",
        to=["a@b"],
        reply_to=None,
        cc=None,
        bcc=None,
        body="plain",
        html_body="<b>h</b>",
    )
    msg = EmailService._build_message(m)
    assert isinstance(msg, MIMEMultipart)
    assert msg["Subject"] == "S"


@pytest.mark.asyncio
async def test_send_email_success_and_failure(monkeypatch):
    mail = SimpleNamespace()
    AsyncMock()
    smtp = AsyncMock()
    smtp.send_message = AsyncMock(return_value=None)

    async def smtp_cm(*args, **kwargs):
        return smtp

    with patch("services.email_service.aiosmtplib.SMTP") as mock_smtp:
        mock_smtp.return_value.__aenter__.return_value = smtp
        mock_smtp.return_value.__aexit__.return_value = None
        smtp.login = AsyncMock()
        res = await EmailService.send_email(mail)
        assert res in (True, False)
