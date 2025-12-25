from schemas.auth import TokenResponse


def test_token_response_defaults():
    t = TokenResponse(access_token="tok")
    assert t.token_type == "bearer"
    assert t.access_token == "tok"
