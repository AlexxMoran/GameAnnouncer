from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .base import Base

if TYPE_CHECKING:
    from .announcement import Announcement
    from .form_field import FormField


class RegistrationForm(Base):
    __tablename__ = "registration_forms"

    announcement_id: Mapped[int] = mapped_column(
        ForeignKey("announcements.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    announcement: Mapped["Announcement"] = relationship(
        "Announcement",
        back_populates="registration_form",
        passive_deletes=True,
        uselist=False,
    )
    fields: Mapped[list["FormField"]] = relationship(
        "FormField", back_populates="form", passive_deletes=True, lazy="selectin"
    )
