from models.game import Game


def test_game_table_and_columns():
    assert Game.__tablename__ == "games"
    cols = Game.__table__.columns
    assert "name" in cols
    assert "description" in cols
    assert "image_url" in cols
    assert "category" in cols


def test_game_relationships():
    rels = {r.key for r in Game.__mapper__.relationships}
    assert "announcements" in rels
