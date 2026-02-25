import pytest
from datetime import datetime, timezone
from domains.games.schemas import GameCreate, GameResponse, GAME_CATEGORIES, GameFilter


def test_game_category_validator_accepts_known_category():
    g = GameCreate(name="G", description="d", category="RTS")
    assert g.category == "RTS"


def test_game_category_validator_case_insensitive():
    g = GameCreate(name="G2", description=None, category="rTs")
    assert g.category.lower() == "rts"


def test_game_category_validator_rejects_invalid():
    with pytest.raises(ValueError):
        GameCreate(name="Bad", description=None, category="UnknownCat")


def test_game_response_fields():
    gr = GameResponse(
        id=1,
        name="N",
        description=None,
        category=GAME_CATEGORIES[0],
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    assert gr.id == 1
    assert hasattr(gr, "announcements_count")


def test_game_filter_all_fields_none():
    filter = GameFilter()
    assert filter.values() == {}


def test_game_filter_with_name():
    filter = GameFilter(name="Dota 2")
    assert filter.values() == {"name": "Dota 2"}


def test_game_filter_with_partial_name():
    filter = GameFilter(name="dota")
    assert filter.values() == {"name": "dota"}


def test_game_filter_excludes_none_values():
    filter = GameFilter(name=None)
    assert filter.values() == {}
    assert "name" not in filter.values()


def test_game_filter_inheritance_from_base_filter():
    filter = GameFilter(name="Test Game")
    assert hasattr(filter, "values")
    assert callable(filter.values)
    assert hasattr(filter, "model_dump")


def test_game_filter_optional_fields():
    filter = GameFilter()
    assert filter.name is None


def test_game_filter_type_validation():
    filter = GameFilter(name="Counter-Strike")
    assert filter.name == "Counter-Strike"
    assert isinstance(filter.name, str)


def test_game_filter_model_dump_exclude_none():
    filter = GameFilter(name=None)
    dumped = filter.model_dump(exclude_none=True)
    assert dumped == {}
    assert "name" not in dumped


def test_game_filter_with_populated_name():
    filter = GameFilter(name="League of Legends")
    dumped = filter.model_dump(exclude_none=True)
    assert dumped == {"name": "League of Legends"}
    assert filter.name == "League of Legends"


def test_game_filter_case_sensitive_storage():
    filter = GameFilter(name="DoTa 2")
    assert filter.name == "DoTa 2"
    assert filter.values() == {"name": "DoTa 2"}


def test_game_filter_empty_string_name():
    filter = GameFilter(name="")
    assert "name" in filter.values()
    assert filter.values() == {"name": ""}


def test_game_filter_whitespace_name():
    filter = GameFilter(name="  Dota 2  ")
    assert filter.name == "  Dota 2  "
    assert filter.values() == {"name": "  Dota 2  "}


def test_game_filter_special_characters():
    filter = GameFilter(name="Game%With_Special")
    assert filter.name == "Game%With_Special"
    assert filter.values() == {"name": "Game%With_Special"}
