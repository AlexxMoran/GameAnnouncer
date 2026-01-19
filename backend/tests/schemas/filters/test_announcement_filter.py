from schemas.filters.announcement_filter import AnnouncementFilter


def test_announcement_filter_all_fields_none():
    """Test that filter with no values returns empty dict"""
    filter = AnnouncementFilter()
    assert filter.values() == {}


def test_announcement_filter_with_game_id():
    """Test filter with only game_id"""
    filter = AnnouncementFilter(game_id=123)
    assert filter.values() == {"game_id": 123}


def test_announcement_filter_with_status():
    """Test filter with only status"""
    filter = AnnouncementFilter(status="registration_open")
    assert filter.values() == {"status": "registration_open"}


def test_announcement_filter_with_all_fields():
    """Test filter with all fields populated"""
    filter = AnnouncementFilter(game_id=456, status="live")
    assert filter.values() == {"game_id": 456, "status": "live"}


def test_announcement_filter_excludes_none_values():
    """Test that None values are excluded from values()"""
    filter = AnnouncementFilter(game_id=789, status=None)
    assert filter.values() == {"game_id": 789}
    assert "status" not in filter.values()


def test_announcement_filter_inheritance_from_base_filter():
    """Test that AnnouncementFilter properly inherits from BaseFilter"""
    filter = AnnouncementFilter(game_id=100)

    # Should have values() method from BaseFilter
    assert hasattr(filter, "values")
    assert callable(filter.values)

    # Should be a Pydantic model
    assert hasattr(filter, "model_dump")


def test_announcement_filter_optional_fields():
    """Test that all fields are optional (can be None)"""
    filter = AnnouncementFilter()
    assert filter.game_id is None
    assert filter.status is None


def test_announcement_filter_type_validation():
    """Test that filter validates field types"""
    filter = AnnouncementFilter(game_id=999)
    assert filter.game_id == 999

    filter = AnnouncementFilter(status="finished")
    assert filter.status == "finished"


def test_announcement_filter_model_dump_exclude_none():
    """Test that model_dump with exclude_none works correctly"""
    filter = AnnouncementFilter(game_id=5, status=None)
    dumped = filter.model_dump(exclude_none=True)

    assert dumped == {"game_id": 5}
    assert "status" not in dumped
