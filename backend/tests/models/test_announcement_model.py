from models.announcement import Announcement


def test_announcement_table_and_columns():
    assert Announcement.__tablename__ == "announcements"
    cols = Announcement.__table__.columns
    assert "title" in cols
    assert "content" in cols
    assert "image_url" in cols
    assert "game_id" in cols
    assert "organizer_id" in cols


def test_announcement_relationships():
    rels = {r.key for r in Announcement.__mapper__.relationships}
    assert "organizer" in rels
    assert "game" in rels
    assert "participants" in rels
    assert "registration_requests" in rels
