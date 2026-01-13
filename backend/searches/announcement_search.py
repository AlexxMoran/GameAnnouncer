from models.announcement import Announcement
from searches.base_search import BaseSearch
from schemas.filters.announcement_filter import AnnouncementFilter


class AnnouncementSearch(BaseSearch):
    model = Announcement
    filter_schema = AnnouncementFilter
