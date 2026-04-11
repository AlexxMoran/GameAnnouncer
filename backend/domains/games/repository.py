from sqlalchemy.ext.asyncio import AsyncSession

from domains.games.model import Game


class GameRepository:
    """Write-side persistence for Game entities."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

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
