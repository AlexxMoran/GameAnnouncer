from .base import Base
from sqlalchemy.orm import (Mapped, mapped_column)


class Game(Base):
    __tablename__ = "games"

    name: Mapped[str] = mapped_column()
