from types import SimpleNamespace
from unittest.mock import MagicMock, patch


def test_verification_email_calls_mail_with_correct_url_and_subject():
    import mailers.user_mailer as um

    with patch(
        "mailers.user_mailer.get_settings",
        return_value=SimpleNamespace(
            cors=SimpleNamespace(frontend_host="https://app.test")
        ),
    ):
        mail_mock = MagicMock(return_value=SimpleNamespace())
        with patch("mailers.base_mailer.BaseMailer.mail", new=mail_mock):
            user_mailer = um.UserMailer()
            email = "u@test"
            token = "tok123"
            user_mailer.verification_email(email=email, token=token, first_name="Joe")

        assert mail_mock.called
        _, kwargs = mail_mock.call_args
        assert kwargs["to"] == email
        assert kwargs["subject"] == "Verify your email address"
        assert kwargs["template"] == "verification_email"
        assert kwargs["first_name"] == "Joe"
        assert (
            kwargs["verification_url"] == "https://app.test/verify-email?token=tok123"
        )


def test_password_reset_email_calls_mail_with_correct_url_and_subject():
    import mailers.user_mailer as um

    with patch(
        "mailers.user_mailer.get_settings",
        return_value=SimpleNamespace(
            cors=SimpleNamespace(frontend_host="https://app.test")
        ),
    ):
        mail_mock = MagicMock(return_value=SimpleNamespace())
        with patch("mailers.base_mailer.BaseMailer.mail", new=mail_mock):
            user_mailer = um.UserMailer()
            email = "r@test"
            token = "reset456"
            user_mailer.password_reset_email(email=email, token=token, first_name=None)

        assert mail_mock.called
        _, kwargs = mail_mock.call_args
        assert kwargs["to"] == email
        assert kwargs["subject"] == "Reset your password"
        assert kwargs["template"] == "password_reset_email"
        assert kwargs["first_name"] is None
        assert kwargs["reset_url"] == "https://app.test/reset-password?token=reset456"
