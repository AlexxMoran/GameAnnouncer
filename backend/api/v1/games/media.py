from fastapi import APIRouter, Depends, File, UploadFile

from core.deps import SessionDep
from core.permissions import authorize_action
from core.schemas.base import DataResponse
from core.services.avatar_uploader import upload_avatar
from core.users import current_user
from modules.games.model import Game
from modules.games.repository import GameRepository
from modules.games.schemas.responses import GameResponse
from modules.users.model import User

from .dependencies import get_game_dependency

router = APIRouter()


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
