from models.announcement_participant import AnnouncementParticipant


def test_tablename_and_columns():
    assert AnnouncementParticipant.__tablename__ == "announcement_participants"

    cols = AnnouncementParticipant.__table__.columns
    assert "id" in cols
    assert "announcement_id" in cols
    assert "user_id" in cols
    assert "qualification_score" in cols
    assert "qualification_rank" in cols
    assert "seed" in cols
    assert "is_qualified" in cols


def test_columns_primary_and_foreign_keys():
    id_col = AnnouncementParticipant.__table__.c["id"]
    announcement_col = AnnouncementParticipant.__table__.c["announcement_id"]
    user_col = AnnouncementParticipant.__table__.c["user_id"]

    assert id_col.primary_key is True
    assert announcement_col.primary_key is False
    assert user_col.primary_key is False
    assert any(
        fk.column.table.name == "announcements" for fk in announcement_col.foreign_keys
    )
    assert any(fk.column.table.name == "users" for fk in user_col.foreign_keys)
