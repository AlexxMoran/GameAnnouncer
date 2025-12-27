from types import SimpleNamespace
from services.permissions_service import PermissionsService
from exceptions.app_exception import AppException


def test_get_permissions_from_policy_handles_no_user():
    class Policy:
        def __init__(self, user, record):
            pass

        def can_edit(self):
            return True

    class Reg:
        def get_policy_methods(self, pc):
            return {"edit": False}

    svc = PermissionsService(Reg())
    perms = svc.get_permissions_from_policy(
        None, object(), Policy, include_global=False
    )
    assert perms["edit"] is False


def test_get_record_permissions_returns_empty_on_registry_error():
    class Reg:
        def get_policy_for_record(self, r):
            raise AppException("no policy")

    svc = PermissionsService(Reg())
    assert svc.get_record_permissions(object(), object()) == {}


def test_get_batch_and_global_permissions():
    class Policy:
        def __init__(self, user, record):
            self.user = user

        def can_view(self):
            return True

        def can_edit(self):
            return False

    class Reg:
        def get_policy_for_record(self, r):
            return Policy

        def get_policy_methods(self, pc):
            return {"view": False, "edit": False}

        def get_all_policies(self):
            return {"Game": Policy}

    svc = PermissionsService(Reg())
    records = [SimpleNamespace(), SimpleNamespace()]
    svc.get_batch_permissions(SimpleNamespace(), records)
    assert hasattr(records[0], "permissions")
    gp = svc.get_global_permissions(SimpleNamespace())
    assert isinstance(gp, dict)
