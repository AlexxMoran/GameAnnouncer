from fastapi import APIRouter, UploadFile, File, Depends

from domains.games.model import Game
from domains.games.repository import GameRepository
from domains.games.schemas import GameCreate, GameResponse, GameUpdate, GameFilter
from domains.games.search import GameSearch
from domains.users.model import User
from exceptions import AppException
from core.services.avatar_uploader import upload_avatar
from core.deps import SessionDep
from core.schemas.base import PaginatedResponse, DataResponse
from core.users import current_user, current_user_or_none
from core.permissions import authorize_action, get_permissions, get_batch_permissions

router = APIRouter(prefix="/games", tags=["games"])


async def get_game_dependency(
    session: SessionDep,
    game_id: int,
) -> Game:
    repo = GameRepository(session)
    game = await repo.find_by_id(game_id)
    if not game:
        raise AppException("Game not found", status_code=404)
    return game


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
    games_count = await search.count()
    get_batch_permissions(user, games)
    return PaginatedResponse(data=games, skip=skip, limit=limit, total=games_count)


@router.get("/{game_id}", response_model=DataResponse[GameResponse])
async def get_game(
    game: Game = Depends(get_game_dependency),
    user: User | None = Depends(current_user_or_none),
) -> DataResponse[GameResponse]:
    game.permissions = get_permissions(user, game)
    return DataResponse(data=game)


@router.post("", response_model=DataResponse[GameResponse])
async def create_game(
    session: SessionDep,
    game_in: GameCreate,
    user: User = Depends(current_user),
) -> DataResponse[GameResponse]:
    authorize_action(user, Game(), "create")
    repo = GameRepository(session)
    game = Game(**game_in.model_dump())
    game = await repo.save(game)
    await session.commit()
    await session.refresh(game)
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


@router.post("/{game_id}/upload_image", response_model=DataResponse[GameResponse])
async def upload_game_image(
    session: SessionDep,
    file: UploadFile = File(...),
    game: Game = Depends(get_game_dependency),
    user: User = Depends(current_user),
) -> DataResponse[GameResponse]:
    authorize_action(user, game, "edit")
    image_url = await upload_avatar(object_type="game", object_id=game.id, file=file)
    game.image_url = image_url
    repo = GameRepository(session)
    game = await repo.save(game)
    await session.commit()
    await session.refresh(game)
    return DataResponse(data=game)
