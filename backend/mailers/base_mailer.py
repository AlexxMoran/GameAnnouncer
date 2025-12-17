from abc import ABC
from bs4 import BeautifulSoup
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from mjml import mjml_to_html

from core.config import settings
from core.logger import logger


@dataclass
class Mail:
    """Email message data."""

    to: str | list[str]
    subject: str
    body: str
    html_body: str | None = None
    from_email: str | None = None
    from_name: str | None = None
    reply_to: str | None = None
    cc: list[str] | None = None
    bcc: list[str] | None = None
    attachments: list[dict[str, Any]] | None = None

    def __post_init__(self):
        if self.from_email is None:
            self.from_email = settings.email.from_email
        if self.from_name is None:
            self.from_name = settings.email.from_name
        if isinstance(self.to, str):
            self.to = [self.to]


class BaseMailer(ABC):
    """Base class for all mailers."""

    def __init__(self):
        self.default_from_email = settings.email.from_email
        self.default_from_name = settings.email.from_name
        self.templates_dir = Path(__file__).parent / "templates"
        self.jinja_env = Environment(loader=FileSystemLoader(str(self.templates_dir)))

    def render_template(self, template_name: str, **context) -> tuple[str, str]:
        """Render MJML template to HTML and plain text."""
        try:
            mjml_template = self.jinja_env.get_template(f"{template_name}.mjml")
        except TemplateNotFound:
            raise FileNotFoundError(
                f"Template '{template_name}.mjml' not found in {self.templates_dir}"
            )

        mjml_content = mjml_template.render(**context)
        result = mjml_to_html(mjml_content)

        if result.get("errors"):
            logger.error(
                f"MJML compilation errors for '{template_name}': {result['errors']}"
            )

        html_body = result.get("html", "")
        plain_body = self._html_to_text(html_body)

        return plain_body, html_body

    def _html_to_text(self, html: str) -> str:
        """Convert HTML to plain text."""
        soup = BeautifulSoup(html, "html.parser")

        return soup.get_text(separator="\n", strip=True)

    def mail(
        self,
        to: str | list[str],
        subject: str,
        template: str | None = None,
        body: str | None = None,
        html_body: str | None = None,
        **kwargs,
    ) -> Mail:
        """Create mail object."""
        if template:
            plain_body, html_body = self.render_template(template, **kwargs)
        else:
            plain_body = body or ""

        return Mail(
            to=to,
            subject=subject,
            body=plain_body,
            html_body=html_body,
            from_email=kwargs.get("from_email"),
            from_name=kwargs.get("from_name"),
            reply_to=kwargs.get("reply_to"),
            cc=kwargs.get("cc"),
            bcc=kwargs.get("bcc"),
            attachments=kwargs.get("attachments"),
        )

    async def deliver(self, mail: Mail) -> bool:
        """Deliver email via SMTP."""
        from services.email_service import EmailService

        return await EmailService.send_email(mail)
