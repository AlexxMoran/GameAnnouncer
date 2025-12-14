"""Permissions system for authorization and access control."""

from core.permissions.facade import (
    authorize_action,
    get_permissions,
    get_batch_permissions,
    get_user_permissions,
    initialize_policies_cache,
)

__all__ = [
    "authorize_action",
    "get_permissions",
    "get_batch_permissions",
    "get_user_permissions",
    "initialize_policies_cache",
]
