from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload


from models.game import Game
from schemas.game import GameCreate, GameUpdate


class GameCRUD:
    async def get_by_id(self, session: AsyncSession, game_id: int) -> Optional[Game]:
        result = await session.execute(
            select(Game)
            .options(selectinload(Game.announcements))
            .where(Game.id == game_id)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self, session: AsyncSession, skip: int = 0, limit: int = 10
    ) -> list[Game]:
        result = await session.execute(
            select(Game).offset(skip).limit(limit).order_by(Game.name.asc())
        )
        return list(result.scalars().all())

    async def create(self, session: AsyncSession, game_in: GameCreate) -> Game:
        game = Game(**game_in.model_dump())
        session.add(game)
        await session.commit()
        await session.refresh(game)

        return game

    async def update(
        self, session: AsyncSession, game: Game, game_in: GameUpdate
    ) -> Game:
        update_data = game_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(game, field, value)

        await session.commit()
        await session.refresh(game)

        return game

    async def delete(self, session: AsyncSession, game: Game) -> None:
        await session.delete(game)
        await session.commit()


game_crud = GameCRUD()
