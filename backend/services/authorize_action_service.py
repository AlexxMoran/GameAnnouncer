from typing import Any

from core.logger import logger
from core.permissions.registry import PoliciesRegistry
from exceptions import AppException
from fastapi import status


class AuthorizationService:
    """Authorizes user actions on records."""

    def __init__(self, registry: PoliciesRegistry):
        self.registry = registry

    def authorize(self, user: Any, record: Any, action: str) -> bool:
        """Authorize action. Raises AppException if denied."""
        policy_class = self.registry.get_policy_for_record(record)
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
        except AppException:
            raise
        except Exception as e:
            logger.error(f"Error in policy check: {e}")
            policy.deny()

        return True
