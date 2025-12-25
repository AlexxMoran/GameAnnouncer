import pytest
from datetime import datetime, timezone
from schemas.game import GameCreate, GameResponse, GAME_CATEGORIES


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
