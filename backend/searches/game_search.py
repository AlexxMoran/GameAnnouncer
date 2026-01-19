from models.game import Game
from searches.base_search import BaseSearch
from schemas.filters.game_filter import GameFilter


class GameSearch(BaseSearch):
    model = Game
    filter_schema = GameFilter
