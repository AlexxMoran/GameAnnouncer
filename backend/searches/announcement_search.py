from sqlalchemy import select, or_, case, desc, func
from sqlalchemy.orm import selectinload, contains_eager

from models.announcement import Announcement
from models.game import Game
from searches.base_search import BaseSearch
from schemas.filters.announcement_filter import AnnouncementFilter


class AnnouncementSearch(BaseSearch):
    model = Announcement
    filter_schema = AnnouncementFilter

    MIN_SEARCH_LENGTH = 2

    def base_query(self):
        query = select(self.model).options(
            selectinload(Announcement.participants),
        )

        query = self.apply_filters(query)

        query = query.order_by(desc(Announcement.created_at))

        return query

    def filter_by_q(self, query, value: str):
        """
        Universal search filter that searches across game.name, announcement.title, and announcement.content.
        Results are prioritized by match location: game.name > title > content.
        Then sorted by created_at DESC (applied in base_query).

        Args:
            query: SQLAlchemy query
            value: Search string (minimum 2 characters, already trimmed by validator)

        Returns:
            Filtered and sorted query
        """
        if len(value) < self.MIN_SEARCH_LENGTH:
            return query

        query = query.join(Game, Announcement.game_id == Game.id).options(
            contains_eager(Announcement.game)
        )

        search_pattern = f"%{value}%"

        search_conditions = or_(
            Game.name.ilike(search_pattern),
            Announcement.title.ilike(search_pattern),
            func.coalesce(Announcement.content, "").ilike(search_pattern),
        )

        query = query.where(search_conditions)

        priority = case(
            (Game.name.ilike(search_pattern), 1),
            (Announcement.title.ilike(search_pattern), 2),
            (func.coalesce(Announcement.content, "").ilike(search_pattern), 3),
            else_=4,
        )

        query = query.order_by(priority)

        return query
