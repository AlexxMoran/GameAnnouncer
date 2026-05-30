from pydantic import Field

from core.search.base_filter import BaseFilter


class AnnouncementFilter(BaseFilter):
    game_id: int | None = None
    status: str | None = None
    q: str | None = Field(None, max_length=100)
