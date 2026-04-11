from sqlalchemy import select, or_, case, desc, func
from sqlalchemy.orm import selectinload

from domains.announcements.model import Announcement
from domains.announcements.schemas import AnnouncementFilter
from domains.games.model import Game
from domains.registration.models import RegistrationForm
from core.search.base_search import BaseSearch


class AnnouncementSearch(BaseSearch):
    model = Announcement
    filter_schema = AnnouncementFilter

    MIN_SEARCH_LENGTH = 2

    def base_query(self):
        query = select(self.model).options(
            selectinload(Announcement.game),
            selectinload(Announcement.participants),
            selectinload(Announcement.registration_form).selectinload(
                RegistrationForm.fields
            ),
        )
        query = self.apply_filters(query)
        query = query.order_by(desc(Announcement.created_at))
        return query

    def filter_by_q(self, query, value: str):
        """
        Universal search filter across game.name, announcement.title, and announcement.content.
        Results are prioritized by match location: game.name > title > content.
        Then sorted by created_at DESC.
        """
        if len(value) < self.MIN_SEARCH_LENGTH:
            return query

        query = query.join(Game, Announcement.game_id == Game.id)

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

        query = query.order_by(priority, desc(Announcement.created_at))

        return query
