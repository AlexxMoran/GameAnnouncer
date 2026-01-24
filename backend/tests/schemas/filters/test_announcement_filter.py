import pytest
from pydantic import ValidationError
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


def test_announcement_filter_search_query_with_q():
    """Test filter with search query parameter"""
    filter = AnnouncementFilter(q="dota")
    assert filter.q == "dota"
    assert filter.values() == {"q": "dota"}


def test_announcement_filter_search_query_trims_whitespace():
    """Test that search query validator trims leading and trailing whitespace"""
    filter = AnnouncementFilter(q="  test query  ")
    assert filter.q == "test query"


def test_announcement_filter_search_query_empty_string_becomes_none():
    """Test that empty string (after trimming) becomes None"""
    filter = AnnouncementFilter(q="   ")
    assert filter.q is None
    assert "q" not in filter.values()


def test_announcement_filter_search_query_none_remains_none():
    """Test that None value remains None"""
    filter = AnnouncementFilter(q=None)
    assert filter.q is None
    assert "q" not in filter.values()


def test_announcement_filter_search_query_preserves_internal_spaces():
    """Test that internal spaces in query are preserved"""
    filter = AnnouncementFilter(q="  counter strike  ")
    assert filter.q == "counter strike"


def test_announcement_filter_with_all_fields_including_q():
    """Test filter with all fields including search query"""
    filter = AnnouncementFilter(game_id=1, status="live", q="tournament")
    assert filter.values() == {"game_id": 1, "status": "live", "q": "tournament"}


def test_announcement_filter_search_query_max_length_valid():
    """Test that search query accepts strings up to 100 characters"""
    valid_query = "a" * 100
    filter = AnnouncementFilter(q=valid_query)
    assert filter.q == valid_query
    assert len(filter.q) == 100


def test_announcement_filter_search_query_max_length_exceeded():
    """Test that search query exceeding 100 characters is rejected"""
    invalid_query = "a" * 101
    with pytest.raises(ValidationError) as exc_info:
        AnnouncementFilter(q=invalid_query)

    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"] == ("q",)
    assert "String should have at most 100 characters" in errors[0]["msg"]
