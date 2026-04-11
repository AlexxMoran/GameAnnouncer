from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from domains.announcements.model import Announcement
from domains.games.model import Game


class GameQueries:
    """Read-side database access for Game entities."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_by_id(self, game_id: int) -> Game | None:
        """
        Fetch a game by ID enriched with announcements count.

        Returns:
            Game with announcements_count attribute set, or None if not found.
        """
        result = await self.session.execute(
            select(Game, func.count(Announcement.id).label("announcements_count"))
            .outerjoin(Announcement, Game.id == Announcement.game_id)
            .where(Game.id == game_id)
            .group_by(Game.id)
        )
        row = result.first()
        if row is None:
            return None

        game, count = row
        game.announcements_count = count
        return game
