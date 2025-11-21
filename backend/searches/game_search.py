from searches.base_search import BaseSearch
from schemas.filters.game_filter import GameFilter
from models.game import Game


class GameSearch(BaseSearch):
    model = Game
    filter_schema = GameFilter
