from typing import TYPE_CHECKING, Optional

from .base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, String, Text

if TYPE_CHECKING:
    from .game import Game
    from .user import User


class Announcement(Base):
    __tablename__ = "announcements"

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

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
