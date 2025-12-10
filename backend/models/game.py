from typing import TYPE_CHECKING, List, Optional
from .base import Base
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .announcement import Announcement


class Game(Base):
    __tablename__ = "games"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False)

    announcements: Mapped[List["Announcement"]] = relationship(
        "Announcement", back_populates="game", cascade="all, delete-orphan"
    )
