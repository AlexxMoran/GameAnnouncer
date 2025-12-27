import pytest

from exceptions.app_exception import AppException


def test_app_exception_defaults():
    exc = AppException("boom")
    assert isinstance(exc, Exception)
    assert exc.message == "boom"
    assert exc.status_code == 500
    assert exc.error_type is None
    assert exc.error is None
    s = str(exc)
    assert "AppException" in s
    assert repr(exc) == s


def test_app_exception_custom_fields_and_str():
    exc = AppException(
        "not found", status_code=404, error_type="NotFound", error={"key": 1}
    )
    assert exc.status_code == 404
    assert exc.message == "not found"
    assert exc.error_type == "NotFound"
    assert exc.error == {"key": 1}
    s = str(exc)
    assert "status_code=404" in s
    assert "not found" in s


def test_app_exception_can_be_raised_and_caught():
    with pytest.raises(AppException) as ctx:
        raise AppException("raise me", status_code=400)

    caught = ctx.value
    assert caught.message == "raise me"
    assert caught.status_code == 400
