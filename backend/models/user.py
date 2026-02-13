from models.base import Base
from typing import TYPE_CHECKING, Optional
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from .announcement import Announcement
    from .registration_request import RegistrationRequest
    from .announcement_participant import AnnouncementParticipant


class User(Base, SQLAlchemyBaseUserTable[int]):
    __tablename__ = "users"

    first_name: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    nickname: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    participation_records: Mapped[list["AnnouncementParticipant"]] = relationship(
        "AnnouncementParticipant",
        back_populates="user",
        passive_deletes=True,
    )

    participated_announcements: AssociationProxy[list["Announcement"]] = (
        association_proxy("participation_records", "announcement")
    )

    organized_announcements: Mapped[list["Announcement"]] = relationship(
        "Announcement", back_populates="organizer", passive_deletes=True
    )

    registration_requests: Mapped[list["RegistrationRequest"]] = relationship(
        "RegistrationRequest", back_populates="user", passive_deletes=True
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
