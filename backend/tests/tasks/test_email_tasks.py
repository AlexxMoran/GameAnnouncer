from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

import tasks.email_tasks as et


@pytest.mark.asyncio
async def test_send_verification_email_task_success():
    mail = SimpleNamespace()
    mock_mailer = SimpleNamespace(
        verification_email=lambda email, token, first_name=None: mail,
        deliver=AsyncMock(return_value=True),
    )

    with patch("tasks.email_tasks.UserMailer", return_value=mock_mailer):
        res = await et.send_verification_email_task("u@t", "tok", "Joe")

    assert res is True
    mock_mailer.deliver.assert_awaited_once_with(mail)


@pytest.mark.asyncio
async def test_send_verification_email_task_failure():
    mail = SimpleNamespace()
    mock_mailer = SimpleNamespace(
        verification_email=lambda email, token, first_name=None: mail,
        deliver=AsyncMock(return_value=False),
    )

    with patch("tasks.email_tasks.UserMailer", return_value=mock_mailer):
        res = await et.send_verification_email_task("u@t", "tok", None)

    assert res is False


@pytest.mark.asyncio
async def test_send_password_reset_email_task_success():
    mail = SimpleNamespace()
    mock_mailer = SimpleNamespace(
        password_reset_email=lambda email, token, first_name=None: mail,
        deliver=AsyncMock(return_value=True),
    )

    with patch("tasks.email_tasks.UserMailer", return_value=mock_mailer):
        res = await et.send_password_reset_email_task("r@t", "rtok", "Ann")

    assert res is True
    mock_mailer.deliver.assert_awaited_once_with(mail)


@pytest.mark.asyncio
async def test_send_password_reset_email_task_failure():
    mail = SimpleNamespace()
    mock_mailer = SimpleNamespace(
        password_reset_email=lambda email, token, first_name=None: mail,
        deliver=AsyncMock(return_value=False),
    )

    with patch("tasks.email_tasks.UserMailer", return_value=mock_mailer):
        res = await et.send_password_reset_email_task("r@t", "rtok", None)

    assert res is False
