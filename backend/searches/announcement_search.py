from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models.announcement import Announcement
from searches.base_search import BaseSearch
from schemas.filters.announcement_filter import AnnouncementFilter


class AnnouncementSearch(BaseSearch):
    model = Announcement
    filter_schema = AnnouncementFilter

    def base_query(self):
        query = select(self.model).options(selectinload(Announcement.participants))
        return self.apply_filters(query)
