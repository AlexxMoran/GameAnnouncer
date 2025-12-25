from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest


def test_mail_defaults_and_to_list():
    import mailers.base_mailer as bm
    from mailers.base_mailer import Mail

    with patch.object(
        bm,
        "settings",
        SimpleNamespace(
            email=SimpleNamespace(from_email="noreply@test", from_name="NoReply")
        ),
    ):
        m = Mail(to="user@example.com", subject="Hi", body="plain")
        assert m.from_email == "noreply@test"
        assert m.from_name == "NoReply"
        assert isinstance(m.to, list) and m.to == ["user@example.com"]


def test_render_template_and_html_to_text():
    import mailers.base_mailer as bm

    from mailers.base_mailer import BaseMailer

    mailer = BaseMailer()

    class FakeTemplate:
        def render(self, **ctx):
            return "<mjml>dummy</mjml>"

    mailer.jinja_env = SimpleNamespace(get_template=lambda name: FakeTemplate())

    with patch.object(
        bm, "mjml_to_html", lambda mjml: {"html": "<h1>Hello</h1>", "errors": []}
    ):
        plain, html = mailer.render_template("any")
    assert "Hello" in plain
    assert html == "<h1>Hello</h1>"


def test_mail_with_template_and_without():
    from mailers.base_mailer import BaseMailer, Mail

    mailer = BaseMailer()

    with patch.object(
        mailer, "render_template", lambda template, **ctx: ("plain text", "<html/>")
    ):
        m = mailer.mail(to="a@b", subject="S", template="t", foo=1)
        assert isinstance(m, Mail)
        assert m.body == "plain text"
        assert m.html_body == "<html/>"

    m2 = mailer.mail(to=["x@x"], subject="S2", body="raw")
    assert m2.body == "raw"


@pytest.mark.asyncio
async def test_deliver_calls_email_service():
    from mailers.base_mailer import BaseMailer, Mail

    mailer = BaseMailer()
    mail = Mail(to="u@t", subject="s", body="b")

    async_mock = AsyncMock(return_value=True)

    with patch("services.email_service.EmailService.send_email", new=async_mock):
        res = await mailer.deliver(mail)
    assert res is True
    async_mock.assert_awaited_once_with(mail)
