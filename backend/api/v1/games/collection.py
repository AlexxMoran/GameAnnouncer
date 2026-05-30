from fastapi import APIRouter, Depends

from core.deps import SessionDep
from core.permissions import authorize_action, get_batch_permissions
from core.schemas.base import DataResponse, PaginatedResponse
from core.users import current_user, current_user_or_none
from modules.games.model import Game
from modules.games.repository import GameRepository
from modules.games.schemas.filters import GameFilter
from modules.games.schemas.mutations import GameCreate
from modules.games.schemas.responses import GameResponse
from modules.games.search import GameSearch
from modules.users.model import User

router = APIRouter()


@router.get("", response_model=PaginatedResponse[GameResponse])
async def get_games(
    session: SessionDep,
    user: User | None = Depends(current_user_or_none),
    filters: GameFilter = Depends(),
    skip: int = 0,
    limit: int = 10,
) -> PaginatedResponse[GameResponse]:
    search = GameSearch(session=session, filters=filters)
    games = await search.results(skip=skip, limit=limit)
    filtered_games_count = await search.filtered_count()
    total_games_count = await search.total_count()
    get_batch_permissions(user, games)
    return PaginatedResponse(
        data=games,
        skip=skip,
        limit=limit,
        filtered_count=filtered_games_count,
        total_count=total_games_count,
    )


@router.post("", response_model=DataResponse[GameResponse])
async def create_game(
    session: SessionDep,
    game_in: GameCreate,
    user: User = Depends(current_user),
) -> DataResponse[GameResponse]:
    authorize_action(user, Game, "create")
    repo = GameRepository(session)
    game = Game(**game_in.model_dump())
    game = await repo.save(game)
    await session.commit()
    await session.refresh(game)
    return DataResponse(data=game)
