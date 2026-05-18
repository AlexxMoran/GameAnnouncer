from pydantic import BaseModel

from modules.announcements.schemas import AnnouncementCreate


class CreateAnnouncementContract(BaseModel):
    """Contract for creating an announcement."""

    announcement_in: AnnouncementCreate
    organizer_id: int
