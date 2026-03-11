import importlib
import pkgutil
import inspect
import threading
from pathlib import Path
from functools import lru_cache
from typing import Any

from core.logger import logger
from exceptions import AppException
from fastapi import status


class PoliciesRegistry:
    """Manages policy discovery and caching.

    Scans both ``core/policies/`` (legacy) and ``domains/*/policy.py`` (new)
    so the two locations can coexist during migration.
    """

    def __init__(self):
        self._cache: dict[str, type] | None = None
        self._lock = threading.Lock()
        self._legacy_policies_dir = Path(__file__).parent.parent / "policies"
        self._domains_dir = Path(__file__).parent.parent.parent / "domains"

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

    def _load_policies_from_dir(
        self, module_prefix: str, policies_dir: Path, skip_names: set[str]
    ) -> dict[str, type]:
        """Discover Policy classes from all modules inside a flat directory."""
        policies: dict[str, type] = {}

        for module_info in pkgutil.iter_modules([str(policies_dir)]):
            if module_info.name in skip_names:
                continue

            module_name = f"{module_prefix}.{module_info.name}"
            try:
                module = importlib.import_module(module_name)
                for attr_name in dir(module):
                    if attr_name.endswith("Policy") and attr_name != "BasePolicy":
                        policy_class = getattr(module, attr_name)
                        if inspect.isclass(policy_class):
                            model_name = attr_name.replace("Policy", "")
                            policies[model_name] = policy_class
            except (ImportError, ModuleNotFoundError, AttributeError) as e:
                logger.warning(f"Failed to import policy module {module_name}: {e}")

        return policies

    def _load_domain_policies(self) -> dict[str, type]:
        """Discover Policy classes from ``domains/<domain>/policy.py`` files."""
        policies: dict[str, type] = {}

        if not self._domains_dir.exists():
            return policies

        for domain_dir in self._domains_dir.iterdir():
            policy_file = domain_dir / "policy.py"
            if not policy_file.exists():
                continue

            module_name = f"domains.{domain_dir.name}.policy"
            try:
                module = importlib.import_module(module_name)
                for attr_name in dir(module):
                    if attr_name.endswith("Policy") and attr_name != "BasePolicy":
                        policy_class = getattr(module, attr_name)
                        if inspect.isclass(policy_class):
                            model_name = attr_name.replace("Policy", "")
                            policies[model_name] = policy_class
            except (ImportError, ModuleNotFoundError, AttributeError) as e:
                logger.warning(f"Failed to import domain policy {module_name}: {e}")

        return policies

    def get_all_policies(self) -> dict[str, type]:
        """Discover all policies from both legacy and domain locations.

        Domain policies take precedence over legacy ones with the same name.
        Thread-safe with double-checked locking.
        """
        if self._cache is not None:
            return self._cache

        with self._lock:
            if self._cache is not None:
                return self._cache

            policies: dict[str, type] = {}

            if self._legacy_policies_dir.exists():
                legacy = self._load_policies_from_dir(
                    "core.policies",
                    self._legacy_policies_dir,
                    skip_names={"base_policy", "permissions"},
                )
                policies.update(legacy)

            domain_policies = self._load_domain_policies()
            policies.update(domain_policies)

            self._cache = policies
            logger.info(f"Discovered {len(policies)} policy classes")
            return policies

    def clear_cache(self):
        """Clear cache (for testing)."""
        with self._lock:
            self._cache = None
            self.get_policy_methods.cache_clear()
