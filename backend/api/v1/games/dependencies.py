from exceptions import AppException
from core.deps import SessionDep
from modules.games.model import Game
from modules.games.queries import GameQueries


async def get_game_dependency(
    session: SessionDep,
    game_id: int,
) -> Game:
    queries = GameQueries(session)
    game = await queries.find_by_id(game_id)
    if not game:
        raise AppException("Game not found", status_code=404)
    return game
