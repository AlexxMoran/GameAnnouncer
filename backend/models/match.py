from sqlalchemy import CheckConstraint, Index, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import DateTime
from datetime import datetime
from typing import TYPE_CHECKING
from .base import Base
from enums import MatchStatus
from exceptions import ValidationException

if TYPE_CHECKING:
    from .announcement import Announcement
    from .announcement_participant import AnnouncementParticipant


class Match(Base):
    """
    Represents a single match in a tournament bracket.

    Supports single-elimination tournaments with:
    - Automatic BYE matches (one participant advances without playing)
    - Third-place playoff matches
    - Match scheduling and completion tracking
    - Score recording and winner determination
    - Bracket navigation via next_match_winner relationship
    """

    __tablename__ = "matches"

    __table_args__ = (
        Index("idx_match_round", "announcement_id", "round_number"),
        UniqueConstraint(
            "announcement_id", "round_number", "match_number", name="uq_match_position"
        ),
        CheckConstraint(
            "(winner_id IS NULL) OR (winner_id = participant1_id) OR (winner_id = participant2_id)",
            name="winner_must_be_participant",
        ),
    )

    announcement_id: Mapped[int] = mapped_column(
        ForeignKey("announcements.id", ondelete="CASCADE"), nullable=False, index=True
    )
    round_number: Mapped[int] = mapped_column(nullable=False)
    match_number: Mapped[int] = mapped_column(nullable=False)
    participant1_id: Mapped[int | None] = mapped_column(
        ForeignKey("announcement_participants.id", ondelete="SET NULL"), nullable=True
    )
    participant2_id: Mapped[int | None] = mapped_column(
        ForeignKey("announcement_participants.id", ondelete="SET NULL"), nullable=True
    )

    participant1_score: Mapped[int | None] = mapped_column(nullable=True)
    participant2_score: Mapped[int | None] = mapped_column(nullable=True)

    winner_id: Mapped[int | None] = mapped_column(
        ForeignKey("announcement_participants.id", ondelete="SET NULL"), nullable=True
    )
    next_match_winner_id: Mapped[int | None] = mapped_column(
        ForeignKey("matches.id", ondelete="SET NULL"), nullable=True
    )

    status: Mapped[str] = mapped_column(
        Enum(MatchStatus, native_enum=False),
        default=MatchStatus.PENDING,
        nullable=False,
        index=True,
    )

    is_bye: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_third_place: Mapped[bool] = mapped_column(default=False, nullable=False)

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    announcement: Mapped["Announcement"] = relationship(
        "Announcement", back_populates="matches", passive_deletes=True
    )
    participant1: Mapped["AnnouncementParticipant | None"] = relationship(
        "AnnouncementParticipant",
        foreign_keys=[participant1_id],
        passive_deletes=True,
    )
    participant2: Mapped["AnnouncementParticipant | None"] = relationship(
        "AnnouncementParticipant",
        foreign_keys=[participant2_id],
        passive_deletes=True,
    )
    winner: Mapped["AnnouncementParticipant | None"] = relationship(
        "AnnouncementParticipant",
        foreign_keys=[winner_id],
        passive_deletes=True,
    )
    next_match_winner: Mapped["Match | None"] = relationship(
        "Match",
        foreign_keys=[next_match_winner_id],
        remote_side="Match.id",
        passive_deletes=True,
    )

    @validates("participant1_score", "participant2_score")
    def validate_scores(self, key: str, value: int | None) -> int | None:
        """Validate that scores are non-negative when set."""
        if value is not None and value < 0:
            raise ValidationException(f"{key} cannot be negative")
        return value

    @validates("round_number", "match_number")
    def validate_numbers(self, key: str, value: int) -> int:
        """Validate that round and match numbers are positive."""
        if value < 1:
            raise ValidationException(f"{key} must be positive (got {value})")
        return value

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"<Match(id={self.id}, "
            f"announcement_id={self.announcement_id}, "
            f"round={self.round_number}, "
            f"match={self.match_number}, "
            f"status={self.status.value if isinstance(self.status, MatchStatus) else self.status})>"
        )
