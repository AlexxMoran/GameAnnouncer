from fastapi import HTTPException, status
from core.logger import logger
from core.utils import camel_to_snake


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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Policy class '{policy_class_name}' not found for record type '{record.__class__.__name__}'.",
        )

    policy = policy_class(user, record)
    method_name = f"can_{action}"

    if not hasattr(policy, method_name):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Policy method '{method_name}' not found in '{policy_class_name}'.",
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
