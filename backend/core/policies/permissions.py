from typing import Any
from fastapi import status
from exceptions import AppException
from core.logger import logger
from core.utils import camel_to_snake
from models.user import User


def authorize_action(user, record, action: str):
    """
    Automatically finds and executes the right policy method.
    Example: authorize_action(current_user, announcement, "edit")
    """

    record_class_name = record.__class__.__name__
    policy_class_name = f"{record_class_name}Policy"
    snake_case_name = camel_to_snake(record_class_name)
    policy_module_name = f"core.policies.{snake_case_name}_policy"

    try:
        module = __import__(policy_module_name, fromlist=[policy_class_name])
        policy_class = getattr(module, policy_class_name)
    except (ModuleNotFoundError, AttributeError):
        raise AppException(
            f"Policy class '{policy_class_name}' not found for record type '{record.__class__.__name__}'",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    policy = policy_class(user, record)
    method_name = f"can_{action}"

    if not hasattr(policy, method_name):
        raise AppException(
            f"Policy method '{method_name}' not found in '{policy_class_name}'",
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
    user: User | None, record: Any, policy_class
) -> dict[str, bool]:
    """
    Automatically extract permissions from policy class.
    Finds all methods starting with 'can_' and checks them.
    """

    if not user:
        permissions = {}
        policy_instance = policy_class(user=None, record=record)
        for method_name in dir(policy_instance):
            if method_name.startswith("can_"):
                action = method_name.replace("can_", "")
                permissions[action] = False
        return permissions

    policy_instance = policy_class(user=user, record=record)
    permissions = {}

    for method_name in dir(policy_instance):
        if method_name.startswith("can_"):
            action = method_name.replace("can_", "")
            try:
                method = getattr(policy_instance, method_name)
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

    record_class_name = record.__class__.__name__
    policy_class_name = f"{record_class_name}Policy"
    snake_case_name = camel_to_snake(record_class_name)
    policy_module_name = f"core.policies.{snake_case_name}_policy"

    try:
        module = __import__(policy_module_name, fromlist=[policy_class_name])
        policy_class = getattr(module, policy_class_name)
    except (ModuleNotFoundError, AttributeError):
        logger.warning(
            f"Policy class '{policy_class_name}' not found for record type '{record_class_name}'"
        )
        return {}

    return get_permissions_from_policy(user, record, policy_class)
