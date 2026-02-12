from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from .base import Base
from enums import FormFieldType

if TYPE_CHECKING:
    from .registration_form import RegistrationForm
    from .form_field_response import FormFieldResponse


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
        comment="The label/question for the form field(Example: 'Nickname in Game')",
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
