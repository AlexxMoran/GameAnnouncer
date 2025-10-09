from typing import Optional
from .base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship, declarative_base
from sqlalchemy import ForeignKey, String, Text


class Announcement(Base):
    __tablename__ = "announcements"

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    game_id: Mapped[int] = mapped_column(
        ForeignKey("games.id", ondelete="CASCADE"),
        nullable=False
    )
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    game: Mapped["Game"] = relationship("Game", back_populates="announcements")

