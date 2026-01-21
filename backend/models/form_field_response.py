from typing import TYPE_CHECKING
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text, UniqueConstraint

if TYPE_CHECKING:
    from .registration_request import RegistrationRequest
    from .form_field import FormField


class FormFieldResponse(Base):
    __tablename__ = "form_field_responses"
    __table_args__ = (
        UniqueConstraint(
            "registration_request_id",
            "form_field_id",
            name="uq_form_field_responses_registration_request_id_form_field_id",
        ),
    )

    registration_request_id: Mapped[int] = mapped_column(
        ForeignKey("registration_requests.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    form_field_id: Mapped[int] = mapped_column(
        ForeignKey("form_fields.id", ondelete="CASCADE"), nullable=False, index=True
    )
    value: Mapped[str] = mapped_column(
        Text, nullable=False, comment="The user's response to the form field"
    )
    registration_request: Mapped["RegistrationRequest"] = relationship(
        "RegistrationRequest", back_populates="form_responses", passive_deletes=True
    )
    form_field: Mapped["FormField"] = relationship(
        "FormField", back_populates="responses", passive_deletes=True
    )
