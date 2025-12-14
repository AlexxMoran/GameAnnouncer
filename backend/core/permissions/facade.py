from typing import Any

from core.permissions.registry import PoliciesRegistry
from services.permissions_service import PermissionsService
from services.authorize_action_service import AuthorizationService

_registry = PoliciesRegistry()
_permissions_service = PermissionsService(_registry)
_authorization_service = AuthorizationService(_registry)


def authorize_action(user, record, action: str):
    """Authorize action. Raises 403 if denied."""
    return _authorization_service.authorize(user, record, action)


def get_permissions(user, record):
    """Get permissions for user on record."""
    return _permissions_service.get_record_permissions(user, record)


def get_batch_permissions(user, records: list["Any"]) -> None:
    """Get batch permissions for user on list of records."""
    return _permissions_service.get_batch_permissions(user, records)


def get_user_permissions(user):
    """Get global permissions for user."""
    return _permissions_service.get_global_permissions(user)


def initialize_policies_cache():
    """Initialize policies cache at startup."""
    _registry.get_all_policies()
