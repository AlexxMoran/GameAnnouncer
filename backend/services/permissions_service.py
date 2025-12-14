from typing import Any

from core.logger import logger
from core.permissions.registry import PoliciesRegistry
from exceptions import AppException
from models.user import User


class PermissionsService:
    """Extracts and checks user permissions."""

    def __init__(self, registry: PoliciesRegistry):
        self.registry = registry

    def get_permissions_from_policy(
        self,
        user: User | None,
        record: Any,
        policy_class: type,
        include_global: bool = False,
    ) -> dict[str, bool]:
        """Extract permissions from policy class."""
        available_methods = self.registry.get_policy_methods(policy_class)
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
            except (AttributeError, TypeError, ValueError) as e:
                logger.error(f"Error checking permission '{action}': {e}")
                permissions[action] = False

        return permissions

    def get_record_permissions(self, user: User | None, record: Any) -> dict[str, bool]:
        """Get permissions for specific record."""
        try:
            policy_class = self.registry.get_policy_for_record(record)
        except AppException:
            logger.warning(
                f"Policy class not found for record type '{record.__class__.__name__}'"
            )
            return {}

        return self.get_permissions_from_policy(
            user, record, policy_class, include_global=False
        )

    def get_batch_permissions(self, user: User | None, records: list[Any]) -> None:
        if not records:
            return

        policy_class = self.registry.get_policy_for_record(records[0])

        for record in records:
            record.permissions = self.get_permissions_from_policy(
                user=user,
                record=record,
                policy_class=policy_class,
                include_global=False,
            )

    def get_global_permissions(self, user: User | None) -> dict[str, dict[str, bool]]:
        """Get global permissions (not tied to objects)."""
        if not user:
            return {}

        all_policies = self.registry.get_all_policies()
        permissions = {}

        for model_name, policy_class in all_policies.items():
            model_permissions = self.get_permissions_from_policy(
                user=user, record=None, policy_class=policy_class, include_global=True
            )

            if model_permissions:
                permissions[model_name.lower()] = model_permissions

        return permissions
