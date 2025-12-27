from exceptions.api_responses import API_RESPONSES


def test_api_responses_has_expected_status_codes():
    expected = {400, 401, 403, 404, 409, 422, 500}
    assert set(API_RESPONSES.keys()) == expected


def test_each_response_has_description_and_content():
    for code, entry in API_RESPONSES.items():
        assert isinstance(code, int)
        assert "description" in entry and isinstance(entry["description"], str)
        assert "content" in entry and isinstance(entry["content"], dict)
        app_json = entry["content"].get("application/json")
        assert isinstance(app_json, dict)
        example = app_json.get("example")
        assert isinstance(example, dict)
        assert "detail" in example and isinstance(example["detail"], str)


def test_validation_error_example_contains_fields():
    example = API_RESPONSES[422]["content"]["application/json"]["example"]
    detail = example["detail"]
    assert "email" in detail and "password" in detail
