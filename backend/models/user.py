from models.base import Base
from typing import TYPE_CHECKING, Optional
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from .announcement import Announcement


class User(Base, SQLAlchemyBaseUserTable[int]):
    __tablename__ = "users"

    first_name: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    nickname: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    participated_announcements: Mapped[list["Announcement"]] = relationship(
        "Announcement",
        secondary="announcement_participants",
        back_populates="participants",
        passive_deletes=True,
    )
    organized_announcements: Mapped[list["Announcement"]] = relationship(
        "Announcement", back_populates="organizer", passive_deletes=True
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
