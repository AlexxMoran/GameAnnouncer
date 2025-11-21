from fastapi import APIRouter, HTTPException, UploadFile, File, Depends

from models.game import Game
from models.user import User
from services.avatar_uploader import AvatarUploader
from core.deps import SessionDep
from api.v1.crud.game import game_crud
from schemas.game import GameCreate, GameResponse, GameUpdate, GameListResponse
from core.users import current_user

router = APIRouter(prefix="/games", tags=["games"])


async def get_game_dependency(
    session: SessionDep,
    game_id: int,
) -> Game:
    game = await game_crud.get_by_id(session=session, game_id=game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

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
        raise HTTPException(status_code=404, detail="Game not found")

    return game


@router.get("/", response_model=GameListResponse)
async def get_games(session: SessionDep, skip: int = 0, limit: int = 10):
    games = await game_crud.get_all(session=session, skip=skip, limit=limit)
    games_count = await game_crud.get_all_count(session=session)

    return GameListResponse(games=games, skip=skip, limit=limit, total=games_count)


@router.get("/{game_id}", response_model=GameResponse)
async def get_game(game: Game = Depends(get_game_dependency)):
    return game


@router.post("/", response_model=GameCreate)
async def create_game(
    session: SessionDep, game_in: GameCreate, current_user: User = Depends(current_user)
):
    game = await game_crud.create(
        session=session, game_in=game_in, user=current_user, action="create"
    )

    return game


@router.put("/{game_id}", response_model=GameUpdate)
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

    return updated_game


@router.post("/{game_id}/upload_image", response_model=GameUpdate)
async def upload_game_image(
    session: SessionDep,
    file: UploadFile = File(...),
    game: Game = Depends(get_game_for_edit_dependency),
):
    image_url = await AvatarUploader.upload_avatar(
        object_type="game", object_id=game.id, file=file
    )

    game.image_url = image_url

    await session.commit()
    await session.refresh(game)

    return game
