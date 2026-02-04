from .base import Base
from typing import TYPE_CHECKING
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Enum, Text
from enums.registration_status import RegistrationStatus

if TYPE_CHECKING:
    from .announcement import Announcement
    from .user import User
    from .form_field_response import FormFieldResponse


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
