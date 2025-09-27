from .base import Base
from sqlalchemy.orm import (Mapped, mapped_column)


class Game(Base):
    name: Mapped[str] = mapped_column()
