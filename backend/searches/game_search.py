from sqlalchemy import func
from models.announcement import Announcement
from searches.base_search import BaseSearch
from schemas.filters.game_filter import GameFilter
from models.game import Game


class GameSearch(BaseSearch):
    model = Game
    filter_schema = GameFilter

    async def results_with_announcements_count(self, skip: int = 0, limit: int = 10):
        query = (
            self.base_query()
            .outerjoin(Announcement, Game.id == Announcement.game_id)
            .add_columns(func.count(Announcement.id).label("announcements_count"))
            .group_by(Game.id)
            .offset(skip)
            .limit(limit)
        )

        result = await self.session.execute(query)
        games_with_counts = result.all()

        for game, count in games_with_counts:
            game.announcements_count = count

        return [game for game, _ in games_with_counts]
