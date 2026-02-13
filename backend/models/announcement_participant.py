from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import ForeignKey, UniqueConstraint, Index
from .base import Base
from exceptions import ValidationException

if TYPE_CHECKING:
    from .announcement import Announcement
    from .user import User


class AnnouncementParticipant(Base):
    __tablename__ = "announcement_participants"

    __table_args__ = (
        UniqueConstraint(
            "announcement_id",
            "user_id",
            name="uq_announcement_participant_announcement_user",
        ),
        Index(
            "ix_announcement_participant_seed_unique",
            "announcement_id",
            "seed",
            unique=True,
            postgresql_where="seed IS NOT NULL",
        ),
        Index(
            "ix_announcement_participant_rank_unique",
            "announcement_id",
            "qualification_rank",
            unique=True,
            postgresql_where="qualification_rank IS NOT NULL",
        ),
    )

    announcement_id: Mapped[int] = mapped_column(
        ForeignKey("announcements.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    qualification_score: Mapped[int | None] = mapped_column(nullable=True)
    qualification_rank: Mapped[int | None] = mapped_column(nullable=True)
    seed: Mapped[int | None] = mapped_column(nullable=True)
    is_qualified: Mapped[bool] = mapped_column(default=False, nullable=False)

    announcement: Mapped["Announcement"] = relationship(
        "Announcement", back_populates="participants", passive_deletes=True
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="participation_records",
        passive_deletes=True,
        lazy="selectin",
    )

    @validates("seed", "qualification_rank", "qualification_score")
    def validate_positive_values(self, key: str, value: int | None) -> int | None:
        """Validate that numeric fields are positive when set."""
        if value is not None and value <= 0:
            raise ValidationException(f"{key} must be a positive number")
        return value

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"<AnnouncementParticipant(id={self.id}, "
            f"announcement_id={self.announcement_id}, "
            f"user_id={self.user_id}, "
            f"seed={self.seed}, "
            f"rank={self.qualification_rank}, "
            f"qualified={self.is_qualified})>"
        )
