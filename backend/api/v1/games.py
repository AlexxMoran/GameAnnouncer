from fastapi import APIRouter, UploadFile, File, Depends

from searches.game_search import GameSearch
from models.game import Game
from models.user import User
from exceptions import AppException
from services.avatar_uploader import upload_avatar
from core.deps import SessionDep
from api.v1.crud.game import game_crud
from schemas.game import GameCreate, GameResponse, GameUpdate
from schemas.base import PaginatedResponse, DataResponse
from core.users import current_user, current_user_or_none
from core.permissions import get_permissions, get_batch_permissions
from schemas.filters.game_filter import GameFilter

router = APIRouter(prefix="/games", tags=["games"])


async def get_game_dependency(
    session: SessionDep,
    game_id: int,
) -> Game:
    game = await game_crud.get_by_id(session=session, game_id=game_id)
    if not game:
        raise AppException("Game not found", status_code=404)

    return game


async def get_game_for_edit_dependency(
    session: SessionDep,
    game_id: int,
    user: User = Depends(current_user),
) -> Game:
    game = await game_crud.get_by_id(
        session=session,
        game_id=game_id,
        user=user,
        action="edit",
    )
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
):
    search = GameSearch(session=session, filters=filters)
    games = await search.results(skip=skip, limit=limit)
    get_batch_permissions(user, games)
    games_count = await search.count()

    return PaginatedResponse(data=games, skip=skip, limit=limit, total=games_count)


@router.get("/{game_id}", response_model=DataResponse[GameResponse])
async def get_game(
    game: Game = Depends(get_game_dependency),
    user: User | None = Depends(current_user_or_none),
):
    game.permissions = get_permissions(user, game)

    return DataResponse(data=game)


@router.post("", response_model=DataResponse[GameResponse])
async def create_game(
    session: SessionDep, game_in: GameCreate, current_user: User = Depends(current_user)
):
    game = await game_crud.create(
        session=session, game_in=game_in, user=current_user, action="create"
    )

    return DataResponse(data=game)


@router.patch("/{game_id}", response_model=DataResponse[GameResponse])
async def update_game(
    session: SessionDep,
    game_in: GameUpdate,
    current_user: User = Depends(current_user),
    game: Game = Depends(get_game_for_edit_dependency),
):
    updated_game = await game_crud.update(
        session=session,
        game=game,
        game_in=game_in,
        user=current_user,
        action="edit",
    )

    return DataResponse(data=updated_game)


@router.delete("/{game_id}", response_model=DataResponse[str])
async def delete_game(
    session: SessionDep,
    game: Game = Depends(get_game_for_edit_dependency),
    current_user: User = Depends(current_user),
):
    await game_crud.delete(
        session=session, game=game, user=current_user, action="delete"
    )

    return DataResponse(data="Game deleted successfully")


@router.post("/{game_id}/upload_image", response_model=DataResponse[GameResponse])
async def upload_game_image(
    session: SessionDep,
    file: UploadFile = File(...),
    game: Game = Depends(get_game_for_edit_dependency),
):
    image_url = await upload_avatar(object_type="game", object_id=game.id, file=file)

    game.image_url = image_url

    await session.commit()
    await session.refresh(game)

    return DataResponse(data=game)

    return game
