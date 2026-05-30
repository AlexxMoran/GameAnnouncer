from modules.games.model import Game
from modules.games.schemas.filters import GameFilter
from core.search.base_search import BaseSearch


class GameSearch(BaseSearch):
    model = Game
    filter_schema = GameFilter
