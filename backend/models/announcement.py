from typing import TYPE_CHECKING, Optional
from datetime import datetime, timezone

from .base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship, validates
from sqlalchemy import ForeignKey, String, Text, DateTime, Enum
from exceptions import ValidationException
from enums import AnnouncementStatus

if TYPE_CHECKING:
    from .game import Game
    from .user import User
    from .registration_request import RegistrationRequest


class Announcement(Base):
    __tablename__ = "announcements"

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    registration_start_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    registration_end_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    status: Mapped[str] = mapped_column(
        Enum(AnnouncementStatus, native_enum=False),
        default=AnnouncementStatus.PRE_REGISTRATION,
        nullable=False,
    )
    max_participants: Mapped[int] = mapped_column(nullable=False)

    game_id: Mapped[int] = mapped_column(
        ForeignKey("games.id", ondelete="CASCADE"), nullable=False
    )
    organizer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    organizer: Mapped["User"] = relationship(
        "User", back_populates="organized_announcements", passive_deletes=True
    )
    game: Mapped["Game"] = relationship(
        "Game", back_populates="announcements", passive_deletes=True
    )

    participants: Mapped[list["User"]] = relationship(
        "User",
        secondary="announcement_participants",
        back_populates="participated_announcements",
        passive_deletes=True,
    )

    registration_requests: Mapped[list["RegistrationRequest"]] = relationship(
        "RegistrationRequest", back_populates="announcement", passive_deletes=True
    )

    @validates("start_at", "registration_start_at", "registration_end_at")
    def validate_datetimes(self, key: str, value: datetime) -> datetime:
        """Validate announcement dates are in correct order."""

        reg_start = getattr(self, "registration_start_at", None)
        reg_end = getattr(self, "registration_end_at", None)
        start = getattr(self, "start_at", None)

        if key == "registration_start_at":
            reg_start = value
        elif key == "registration_end_at":
            reg_end = value
        elif key == "start_at":
            start = value

        if reg_start and reg_end and reg_start >= reg_end:
            raise ValidationException(
                "registration_start_at must be before registration_end_at"
            )

        if reg_end and start and start < reg_end:
            raise ValidationException(
                "start_at must be after or equal to registration_end_at"
            )

        return value

    @property
    def is_registration_open(self) -> bool:
        """Check if the registration is currently open."""

        now = datetime.now(timezone.utc)

        return self.registration_start_at <= now <= self.registration_end_at
