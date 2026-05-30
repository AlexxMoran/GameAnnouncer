from fastapi import APIRouter, Depends

from core.deps import SessionDep
from core.permissions import authorize_action, get_permissions
from core.schemas.base import DataResponse
from core.users import current_user, current_user_or_none
from modules.games.model import Game
from modules.games.repository import GameRepository
from modules.games.schemas.mutations import GameUpdate
from modules.games.schemas.responses import GameResponse
from modules.users.model import User

from .dependencies import get_game_dependency

router = APIRouter()


@router.get("/{game_id}", response_model=DataResponse[GameResponse])
async def get_game(
    game: Game = Depends(get_game_dependency),
    user: User | None = Depends(current_user_or_none),
) -> DataResponse[GameResponse]:
    game.permissions = get_permissions(user, game)
    return DataResponse(data=game)


@router.patch("/{game_id}", response_model=DataResponse[GameResponse])
async def update_game(
    session: SessionDep,
    game_in: GameUpdate,
    game: Game = Depends(get_game_dependency),
    user: User = Depends(current_user),
) -> DataResponse[GameResponse]:
    authorize_action(user, game, "edit")
    repo = GameRepository(session)
    for field, value in game_in.model_dump(exclude_unset=True).items():
        setattr(game, field, value)
    game = await repo.save(game)
    await session.commit()
    await session.refresh(game)
    return DataResponse(data=game)


@router.delete("/{game_id}", response_model=DataResponse[str])
async def delete_game(
    session: SessionDep,
    game: Game = Depends(get_game_dependency),
    user: User = Depends(current_user),
) -> DataResponse[str]:
    authorize_action(user, game, "delete")
    repo = GameRepository(session)
    await repo.delete(game)
    await session.commit()
    return DataResponse(data="Game deleted successfully")
