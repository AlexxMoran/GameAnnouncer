from schemas.filters.game_filter import GameFilter


def test_game_filter_values_excludes_none():
    f = GameFilter()
    assert f.values() == {}
    f2 = GameFilter(category="RTS")
    assert f2.values() == {"category": "RTS"}
