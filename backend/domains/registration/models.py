from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, Enum, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB

from core.db.base import Base
from enums import FormFieldType
from enums.registration_status import RegistrationStatus

if TYPE_CHECKING:
    from domains.announcements.model import Announcement
    from domains.users.model import User


class RegistrationForm(Base):
    __tablename__ = "registration_forms"

    announcement_id: Mapped[int] = mapped_column(
        ForeignKey("announcements.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    announcement: Mapped["Announcement"] = relationship(
        "Announcement",
        back_populates="registration_form",
        passive_deletes=True,
        uselist=False,
    )
    fields: Mapped[list["FormField"]] = relationship(
        "FormField", back_populates="form", passive_deletes=True, lazy="selectin"
    )


class FormField(Base):
    __tablename__ = "form_fields"

    form_id: Mapped[int] = mapped_column(
        ForeignKey("registration_forms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    field_type: Mapped[str] = mapped_column(
        Enum(FormFieldType, native_enum=False, validate_strings=True),
        nullable=False,
        comment="The type of the form field (Example: 'text', 'select', 'checkbox')",
    )
    label: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="The label/question for the form field (Example: 'Nickname in Game')",
    )
    required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Whether this field is required or optional",
    )
    options: Mapped[list[str] | None] = mapped_column(
        JSONB,
        nullable=True,
        comment="The options for fields like selects, dropdowns or multiple choice",
    )

    form: Mapped["RegistrationForm"] = relationship(
        "RegistrationForm", back_populates="fields", passive_deletes=True
    )
    responses: Mapped[list["FormFieldResponse"]] = relationship(
        "FormFieldResponse", back_populates="form_field", passive_deletes=True
    )


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
        "FormField", back_populates="responses", passive_deletes=True, lazy="selectin"
    )


class RegistrationRequest(Base):
    __tablename__ = "registration_requests"

    announcement_id: Mapped[int] = mapped_column(
        ForeignKey("announcements.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str] = mapped_column(
        Enum(RegistrationStatus), default=RegistrationStatus.PENDING, nullable=False
    )
    cancellation_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Reason for cancellation/decline of the registration request",
    )

    announcement: Mapped["Announcement"] = relationship(
        "Announcement", back_populates="registration_requests", passive_deletes=True
    )
    user: Mapped["User"] = relationship(
        "User", back_populates="registration_requests", passive_deletes=True
    )
    form_responses: Mapped[list["FormFieldResponse"]] = relationship(
        "FormFieldResponse",
        back_populates="registration_request",
        passive_deletes=True,
        lazy="selectin",
    )
