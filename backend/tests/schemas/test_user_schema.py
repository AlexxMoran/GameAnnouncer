from schemas.user import UserResponse, UserCreate


def test_user_schemas_have_optional_fields_and_permissions():
    uc = UserCreate(email="a@b.com", password="pw")
    assert uc.email == "a@b.com"
    ur = UserResponse(id=1, email="a@b.com", is_active=True, is_superuser=False)
    assert ur.permissions == {}
