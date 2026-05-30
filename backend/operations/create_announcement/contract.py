from pydantic import BaseModel

from modules.announcements.schemas.mutations import AnnouncementCreate


class CreateAnnouncementContract(BaseModel):
    """Contract for creating an announcement."""

    announcement_in: AnnouncementCreate
    organizer_id: int
