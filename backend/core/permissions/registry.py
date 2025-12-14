import importlib
import pkgutil
import inspect
import threading
from pathlib import Path
from functools import lru_cache
from typing import Any

from core.logger import logger
from core.utils import camel_to_snake
from exceptions import AppException
from fastapi import status


class PoliciesRegistry:
    """Manages policy discovery and caching."""

    def __init__(self):
        self._cache: dict[str, type] | None = None
        self._lock = threading.Lock()
        self._policies_dir = Path(__file__).parent.parent / "policies"

    @lru_cache(maxsize=128)
    def get_policy_methods(self, policy_class: type) -> dict[str, bool]:
        """Get cached methods: {"edit": False, "create": True} (value = is_global)."""
        from core.permissions.constants import GLOBAL_PERMISSIONS

        methods = {}
        for method_name in dir(policy_class):
            if method_name.startswith("can_") and not method_name.startswith("_"):
                action = method_name.replace("can_", "")
                methods[action] = action in GLOBAL_PERMISSIONS
        return methods

    def get_policy_for_record(self, record: Any) -> type:
        """Find policy class for a record."""
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

    def get_all_policies(self) -> dict[str, type]:
        """Discover all policies. Thread-safe with double-checked locking."""
        if self._cache is not None:
            return self._cache

        with self._lock:
            if self._cache is not None:
                return self._cache

            policies = {}

            for module_info in pkgutil.iter_modules([str(self._policies_dir)]):
                if module_info.name in ("base_policy", "permissions"):
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

            self._cache = policies
            logger.info(f"Discovered {len(policies)} policy classes")
            return policies

    def clear_cache(self):
        """Clear cache (for testing)."""
        with self._lock:
            self._cache = None
            self.get_policy_methods.cache_clear()
