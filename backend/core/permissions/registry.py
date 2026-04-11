import importlib
import inspect
import threading
from pathlib import Path
from functools import lru_cache
from typing import Any

from core.logger import logger
from core.permissions.base_policy import BasePolicy as _BasePolicy
from exceptions import AppException
from fastapi import status


class PoliciesRegistry:
    """Manages policy discovery and caching.

    Scans ``domains/*/policy.py`` files to discover all concrete policy classes.
    """

    def __init__(self):
        self._cache: dict[str, type] | None = None
        self._lock = threading.Lock()
        self._domains_dir = Path(__file__).parent.parent.parent / "domains"

    @staticmethod
    @lru_cache(maxsize=None)
    def get_policy_methods(policy_class: type) -> dict[str, bool]:
        """Get cached methods: {"edit": False, "create": True} (value = is_global)."""
        from core.permissions.constants import GLOBAL_PERMISSIONS

        methods = {}
        for method_name in dir(policy_class):
            if method_name.startswith("can_"):
                action = method_name.replace("can_", "")
                methods[action] = action in GLOBAL_PERMISSIONS
        return methods

    def get_policy_for_record(self, record: Any) -> type:
        """Find policy class for a record using the discovered policy cache.

        Accepts either a model instance or the model class itself.  Passing the
        class is the preferred form for resource-agnostic checks (e.g. 'create')
        because it avoids constructing a throwaway ORM object.
        """
        if isinstance(record, type):
            record_class_name = record.__name__
        else:
            record_class_name = record.__class__.__name__
        policy_class_name = f"{record_class_name}Policy"
        all_policies = self.get_all_policies()

        policy_class = all_policies.get(record_class_name)
        if policy_class is None:
            raise AppException(
                f"Policy class '{policy_class_name}' not found for record type '{record_class_name}'",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return policy_class

    def _load_domain_policies(self) -> dict[str, type]:
        """Discover Policy classes from ``domains/<domain>/policy.py`` files."""
        policies: dict[str, type] = {}

        if not self._domains_dir.exists():
            return policies

        for domain_dir in sorted(self._domains_dir.iterdir()):
            if not domain_dir.is_dir():
                continue
            policy_file = domain_dir / "policy.py"
            if not policy_file.exists():
                continue

            module_name = f"domains.{domain_dir.name}.policy"
            try:
                module = importlib.import_module(module_name)
                for attr_name in dir(module):
                    policy_class = getattr(module, attr_name)
                    if not (
                        inspect.isclass(policy_class)
                        and issubclass(policy_class, _BasePolicy)
                        and policy_class is not _BasePolicy
                    ):
                        continue
                    model_name = attr_name.replace("Policy", "")
                    if model_name in policies:
                        logger.warning(
                            "Policy key '%s' already registered by '%s'; overwriting with '%s'",
                            model_name,
                            policies[model_name].__module__,
                            policy_class.__module__,
                        )
                    policies[model_name] = policy_class
            except (ImportError, AttributeError) as e:
                logger.warning("Failed to import domain policy %s: %s", module_name, e)

        return policies

    def get_all_policies(self) -> dict[str, type]:
        """Discover all policies from ``domains/*/policy.py``.

        Thread-safe with double-checked locking.
        """
        if self._cache is not None:
            return self._cache

        with self._lock:
            if self._cache is not None:
                return self._cache

            policies = self._load_domain_policies()

            self._cache = policies
            logger.info(f"Discovered {len(policies)} policy classes")
            return policies

    def clear_cache(self):
        """Clear cache (for testing)."""
        with self._lock:
            self._cache = None
            PoliciesRegistry.get_policy_methods.cache_clear()
