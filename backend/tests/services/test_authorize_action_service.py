import pytest

from services.authorize_action_service import AuthorizationService
from exceptions.app_exception import AppException


def test_authorize_raises_if_user_none():
    registry = type("R", (), {"get_policy_for_record": lambda self, r: None})()
    svc = AuthorizationService(registry)
    with pytest.raises(AppException):
        svc.authorize(None, object(), "edit")


def test_authorize_raises_if_policy_missing_method():
    class FakeRegistry:
        def get_policy_for_record(self, record):
            class P:
                def __init__(self, user, record):
                    pass

            return P

    svc = AuthorizationService(FakeRegistry())
    with pytest.raises(AppException):
        svc.authorize(object(), object(), "missing")


def test_authorize_calls_policy_method_and_allows_true(monkeypatch):
    called = {}

    class FakePolicy:
        def __init__(self, user, record):
            pass

        def can_edit(self):
            called["ok"] = True
            return True

    class FakeRegistry:
        def get_policy_for_record(self, record):
            return FakePolicy

    svc = AuthorizationService(FakeRegistry())
    res = svc.authorize(object(), object(), "edit")
    assert res is True
