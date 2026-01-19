from schemas.filters.game_filter import GameFilter


def test_game_filter_all_fields_none():
    """Test that filter with no values returns empty dict"""
    filter = GameFilter()
    assert filter.values() == {}


def test_game_filter_with_name():
    """Test filter with only name"""
    filter = GameFilter(name="Dota 2")
    assert filter.values() == {"name": "Dota 2"}


def test_game_filter_with_partial_name():
    """Test filter with partial name"""
    filter = GameFilter(name="dota")
    assert filter.values() == {"name": "dota"}


def test_game_filter_excludes_none_values():
    """Test that None values are excluded from values()"""
    filter = GameFilter(name=None)
    assert filter.values() == {}
    assert "name" not in filter.values()


def test_game_filter_inheritance_from_base_filter():
    """Test that GameFilter properly inherits from BaseFilter"""
    filter = GameFilter(name="Test Game")

    # Should have values() method from BaseFilter
    assert hasattr(filter, "values")
    assert callable(filter.values)

    # Should be a Pydantic model
    assert hasattr(filter, "model_dump")


def test_game_filter_optional_fields():
    """Test that all fields are optional (can be None)"""
    filter = GameFilter()
    assert filter.name is None


def test_game_filter_type_validation():
    """Test that filter validates field types"""
    filter = GameFilter(name="Counter-Strike")
    assert filter.name == "Counter-Strike"
    assert isinstance(filter.name, str)


def test_game_filter_model_dump_exclude_none():
    """Test that model_dump with exclude_none works correctly"""
    filter = GameFilter(name=None)
    dumped = filter.model_dump(exclude_none=True)

    assert dumped == {}
    assert "name" not in dumped


def test_game_filter_with_populated_name():
    """Test filter with name populated"""
    filter = GameFilter(name="League of Legends")
    dumped = filter.model_dump(exclude_none=True)

    assert dumped == {"name": "League of Legends"}
    assert filter.name == "League of Legends"


def test_game_filter_case_sensitive_storage():
    """Test that filter stores name with original case"""
    filter = GameFilter(name="DoTa 2")
    assert filter.name == "DoTa 2"  # Preserves original case
    assert filter.values() == {"name": "DoTa 2"}


def test_game_filter_empty_string_name():
    """Test that empty string is preserved (not treated as None)"""
    filter = GameFilter(name="")
    # Empty string should be included in values
    assert "name" in filter.values()
    assert filter.values() == {"name": ""}


def test_game_filter_whitespace_name():
    """Test that whitespace in name is preserved"""
    filter = GameFilter(name="  Dota 2  ")
    assert filter.name == "  Dota 2  "
    assert filter.values() == {"name": "  Dota 2  "}


def test_game_filter_special_characters():
    """Test that special characters are preserved"""
    filter = GameFilter(name="Game%With_Special")
    assert filter.name == "Game%With_Special"
    assert filter.values() == {"name": "Game%With_Special"}
