from fastapi import APIRouter, HTTPException, UploadFile, File

from services.avatar_uploader import AvatarUploader
from core.deps import SessionDep
from api.v1.crud.game import game_crud
from schemas.game import GameCreate, GameResponse, GameUpdate

router = APIRouter(prefix="/games", tags=["games"])

@router.get("/", response_model=list[GameResponse])
async def get_games(session: SessionDep, skip: int = 0, limit: int = 10):
    games = await game_crud.get_all(session=session, skip=skip, limit=limit)

    return games

@router.get("/{game_id}", response_model=GameResponse)
async def get_game(session: SessionDep, game_id: int):
    game = await game_crud.get_by_id(session=session, game_id=game_id)

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    return game

@router.post("/", response_model=GameCreate)
async def create_game(session: SessionDep, game: GameCreate):
    game = await game_crud.create(session=session, game_in=game)

    return game

@router.put("/{game_id}", response_model=GameUpdate)
async def update_game(session: SessionDep, game_id: int, game: GameUpdate):
    game_object = await game_crud.get_by_id(session=session, game_id=game_id)

    if not game_object:
        raise HTTPException(status_code=404, detail="Game not found")

    game = await game_crud.update(session=session, game=game_object, game_in=game)

    return game

@router.post("/{game_id}/upload_image", response_model=GameUpdate)
async def upload_game_image(session: SessionDep, game_id: int, file: UploadFile = File(...)):
    game = await game_crud.get_by_id(session=session, game_id=game_id)

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    image_url = await AvatarUploader.upload_avatar(object_type="game", object_id=game_id, file=file)

    game.image_url = image_url
    
    await session.commit()
    await session.refresh(game)

    return game

