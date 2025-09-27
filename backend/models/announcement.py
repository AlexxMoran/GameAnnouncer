from .base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship, declarative_base
from sqlalchemy import ForeignKey


class Announcement(Base):
    __tablename__ = "announcements"

    game_id: Mapped[int] = mapped_column(
        ForeignKey("games.id", ondelete="CASCADE"),
        nullable=False
    )

    game: Mapped["Game"] = relationship("Game", back_populates="announcements")

