from models.user import User


def test_user_table_and_relationships():
    assert User.__tablename__ == "users"
    rels = {r.key for r in User.__mapper__.relationships}
    assert "participated_announcements" in rels
    assert "organized_announcements" in rels
    assert "registration_requests" in rels


def test_user_get_db_callable():
    assert callable(getattr(User, "get_db"))
