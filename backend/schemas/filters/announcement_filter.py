from .base_filter import BaseFilter


class AnnouncementFilter(BaseFilter):
    game_id: int | None = None
    status: str | None = None
