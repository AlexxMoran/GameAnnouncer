from pydantic import BaseModel


class FinalizeAnnouncementQualificationContract(BaseModel):
    """Contract for finalizing an announcement qualification stage."""

    announcement_id: int
