from pydantic import BaseModel

from modules.announcements.schemas.mutations import AnnouncementUpdate


class UpdateAnnouncementContract(BaseModel):
    """Contract for updating an announcement."""

    announcement_id: int
    announcement_in: AnnouncementUpdate
