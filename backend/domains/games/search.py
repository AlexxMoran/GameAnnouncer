from domains.games.model import Game
from domains.games.schemas import GameFilter
from core.search.base_search import BaseSearch


class GameSearch(BaseSearch):
    model = Game
    filter_schema = GameFilter
