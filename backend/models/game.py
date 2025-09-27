from typing import List
from .base import Base
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Game(Base):
    __tablename__ = "games"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    announcements: Mapped[List["Announcement"]] = relationship(
        "Announcement",
        back_populates="game",
        cascade="all, delete-orphan"
    )
