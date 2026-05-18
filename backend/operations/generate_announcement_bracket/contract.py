from pydantic import BaseModel


class GenerateAnnouncementBracketContract(BaseModel):
    """Contract for generating an announcement tournament bracket."""

    announcement_id: int
