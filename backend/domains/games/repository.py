from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from domains.games.model import Game
from domains.announcements.model import Announcement


class GameRepository:
    """Data access layer for Game entities."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_by_id(self, game_id: int) -> Game | None:
        """
        Find a game by ID, enriched with announcements count.

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
        if not row:
            return None
        game, count = row
        game.announcements_count = count
        return game

    async def find_all(self, skip: int = 0, limit: int = 10) -> tuple[list[Game], int]:
        """
        Find all games with pagination.

        Returns:
            Tuple of (games list, total count).
        """
        count_result = await self.session.execute(select(func.count(Game.id)))
        total = count_result.scalar_one()

        data_result = await self.session.execute(
            select(Game).offset(skip).limit(limit).order_by(Game.name.asc())
        )
        games = list(data_result.scalars().all())
        return games, total

    async def save(self, game: Game) -> Game:
        """
        Persist a game (insert or update).

        Flushes to DB to generate ID but does not commit — caller owns the transaction.

        Returns:
            Refreshed Game instance.
        """
        self.session.add(game)
        await self.session.flush()
        await self.session.refresh(game)
        return game

    async def delete(self, game: Game) -> None:
        """
        Delete a game.

        Flushes but does not commit — caller owns the transaction.
        """
        await self.session.delete(game)
        await self.session.flush()
