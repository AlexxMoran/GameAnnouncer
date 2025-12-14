from typing import Any
import importlib
import pkgutil
from pathlib import Path
import inspect
from fastapi import status
from functools import lru_cache
from exceptions import AppException
from core.logger import logger
from core.utils import camel_to_snake
from models.user import User

GLOBAL_PERMISSIONS = ["create"]

_POLICIES_CACHE = None


@lru_cache(maxsize=128)
def _get_policy_methods(policy_class: type) -> dict[str, bool]:
    """
    Cache policy methods for a given policy class.
    Returns: {"edit": False, "delete": False, "create": True} where value indicates if it's global.
    """
    methods = {}
    for method_name in dir(policy_class):
        if method_name.startswith("can_") and not method_name.startswith("_"):
            action = method_name.replace("can_", "")
            methods[action] = action in GLOBAL_PERMISSIONS
    return methods


def _get_policy_class(record: Any) -> type:
    """
    Find and import policy class for a given record.
    """
    record_class_name = record.__class__.__name__
    policy_class_name = f"{record_class_name}Policy"
    snake_case_name = camel_to_snake(record_class_name)
    policy_module_name = f"core.policies.{snake_case_name}_policy"

    try:
        module = __import__(policy_module_name, fromlist=[policy_class_name])
        policy_class = getattr(module, policy_class_name)
        return policy_class
    except (ModuleNotFoundError, AttributeError) as e:
        raise AppException(
            f"Policy class '{policy_class_name}' not found for record type '{record_class_name}'",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) from e


def authorize_action(user, record, action: str):
    """
    Automatically finds and executes the right policy method.
    Example: authorize_action(current_user, announcement, "edit")
    """

    policy_class = _get_policy_class(record)
    policy = policy_class(user, record)
    method_name = f"can_{action}"

    if not hasattr(policy, method_name):
        raise AppException(
            f"Policy method '{method_name}' not found in '{policy_class.__name__}'",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    try:
        policy_method = getattr(policy, method_name)
        can_perform_action = policy_method()

        if not can_perform_action:
            policy.deny()
    except Exception as e:
        logger.error(f"Error in policy check: {e}")
        policy.deny()

    return True


def get_permissions_from_policy(
    user: User | None, record: Any, policy_class, include_global: bool = False
) -> dict[str, bool]:
    """
    Automatically extract permissions from policy class.
    Uses cached method discovery for performance.

    Args:
        user: User to check permissions for
        record: Object to check permissions against (can be None for global permissions)
        policy_class: Policy class to use
        include_global: If True, include only global permissions. If False, exclude global permissions.

    Returns:
        Dictionary of permissions like {"edit": True, "delete": False}
    """

    available_methods = _get_policy_methods(policy_class)

    policy_instance = policy_class(user=user, record=record)
    permissions = {}

    for action, is_global in available_methods.items():
        if include_global != is_global:
            continue

        if not user:
            permissions[action] = False
            continue

        try:
            method = getattr(policy_instance, f"can_{action}")
            if callable(method):
                permissions[action] = method()
        except Exception as e:
            logger.error(f"Error checking permission '{action}': {e}")
            permissions[action] = False

    return permissions


def get_permissions(user: User | None, record: Any) -> dict[str, bool]:
    """
    Universal function that finds policy by model class name and returns permissions.
    Usage: game.permissions = get_permissions(current_user, game)
    """

    try:
        policy_class = _get_policy_class(record)
    except AppException:
        logger.warning(
            f"Policy class not found for record type '{record.__class__.__name__}'"
        )
        return {}

    return get_permissions_from_policy(user, record, policy_class)


def _discover_all_policies() -> dict[str, type]:
    """
    Automatically discover all policy classes in core/policies/ directory.
    Returns: {"Game": GamePolicy, "Announcement": AnnouncementPolicy, ...}
    """
    global _POLICIES_CACHE

    if _POLICIES_CACHE is not None:
        return _POLICIES_CACHE

    policies = {}
    policies_dir = Path(__file__).parent

    for module_info in pkgutil.iter_modules([str(policies_dir)]):
        if module_info.name in ("base_policy", "permissions", "authorize_action"):
            continue

        module_name = f"core.policies.{module_info.name}"

        try:
            module = importlib.import_module(module_name)

            for attr_name in dir(module):
                if attr_name.endswith("Policy") and attr_name != "BasePolicy":
                    policy_class = getattr(module, attr_name)

                    if inspect.isclass(policy_class):
                        model_name = attr_name.replace("Policy", "")
                        policies[model_name] = policy_class

        except Exception as e:
            logger.warning(f"Failed to import policy module {module_name}: {e}")

    _POLICIES_CACHE = policies
    return policies


def get_user_permissions(user: User | None) -> dict[str, dict[str, bool]]:
    """
    Get global permissions for user that are not tied to specific objects.
    Automatically discovers all policies and checks methods defined in GLOBAL_PERMISSIONS.

    Only processes methods matching GLOBAL_PERMISSIONS list (like 'can_create').
    Methods that require a specific object (like 'can_edit', 'can_delete') are excluded.

    Returns: {
        "game": {"create": True},
        "announcement": {"create": True}
    }
    """

    if not user:
        return {}

    all_policies = _discover_all_policies()
    permissions = {}

    for model_name, policy_class in all_policies.items():
        model_permissions = get_permissions_from_policy(
            user=user, record=None, policy_class=policy_class, include_global=True
        )

        if model_permissions:
            permissions[model_name.lower()] = model_permissions

    return permissions
