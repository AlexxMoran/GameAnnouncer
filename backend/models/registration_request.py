from .base import Base
from typing import TYPE_CHECKING
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Enum
from enums.registration_status import RegistrationStatus

if TYPE_CHECKING:
    from .announcement import Announcement
    from .user import User


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

    announcement: Mapped["Announcement"] = relationship(
        "Announcement", back_populates="registration_requests", passive_deletes=True
    )

    user: Mapped["User"] = relationship(
        "User", back_populates="registration_requests", passive_deletes=True
    )
