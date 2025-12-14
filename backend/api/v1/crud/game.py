from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select


from models.announcement import Announcement
from core.permissions import authorize_action
from models.game import Game
from models.user import User
from schemas.game import GameCreate, GameUpdate


class GameCRUD:
    async def get_by_id(
        self,
        session: AsyncSession,
        game_id: int,
        user: Optional[User] = None,
        action: Optional[str] = None,
    ) -> Optional[Game]:
        result = await session.execute(
            select(Game, func.count(Announcement.id).label("announcements_count"))
            .outerjoin(Announcement, Game.id == Announcement.game_id)
            .where(Game.id == game_id)
            .group_by(Game.id)
        )

        row = result.first()
        if row:
            game, count = row
            game.announcements_count = count

            if user and action:
                authorize_action(user, game, action)

            return game

        return None

    async def get_all(
        self, session: AsyncSession, skip: int = 0, limit: int = 10
    ) -> list[Game]:
        result = await session.execute(
            select(Game).offset(skip).limit(limit).order_by(Game.name.asc())
        )
        return list(result.scalars().all())

    async def get_all_count(self, session: AsyncSession) -> int:
        result = await session.execute(select(func.count(Game.id)))
        return result.scalar_one()

    async def create(
        self,
        session: AsyncSession,
        game_in: GameCreate,
        user: Optional[User] = None,
        action: Optional[str] = None,
    ) -> Game:
        authorize_action(user, Game(), action)

        game = Game(**game_in.model_dump())
        session.add(game)
        await session.commit()
        await session.refresh(game)

        return game

    async def update(
        self,
        session: AsyncSession,
        game: Game,
        game_in: GameUpdate,
        user: Optional[User] = None,
        action: Optional[str] = None,
    ) -> Game:
        authorize_action(user, Game(), action)

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
