from pydantic import Field, field_validator
from .base_filter import BaseFilter


class AnnouncementFilter(BaseFilter):
    game_id: int | None = None
    status: str | None = None
    q: str | None = Field(None, max_length=100)

    @field_validator("q")
    @classmethod
    def validate_search_query(cls, v: str | None) -> str | None:
        """
        Validate search query: trim whitespace and return None for empty strings.

        Args:
            v: Search query string or None

        Returns:
            Trimmed string or None if empty/whitespace-only
        """
        if v is None:
            return v

        v = v.strip()

        if not v:
            return None

        return v
