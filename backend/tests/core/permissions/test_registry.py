import logging
import types
from pathlib import Path
from unittest.mock import patch


from core.permissions.base_policy import BasePolicy
from core.permissions.registry import PoliciesRegistry


def make_registry(domains_dir: Path) -> PoliciesRegistry:
    """Return a fresh registry pointed at *domains_dir* instead of the real domains/."""
    reg = PoliciesRegistry()
    reg._domains_dir = domains_dir
    return reg


def fake_policy_module(name: str, policy_class: type) -> types.ModuleType:
    """Build a minimal module object that exposes *policy_class* by its __name__."""
    mod = types.ModuleType(name)
    setattr(mod, policy_class.__name__, policy_class)
    return mod


class SamplePolicy(BasePolicy):
    """Minimal concrete policy used across several tests."""

    def can_view(self) -> bool:
        return True


class OtherPolicy(BasePolicy):
    """Second concrete policy for collision tests."""

    def can_view(self) -> bool:
        return False


def test_load_returns_empty_when_domains_dir_missing():
    """Missing domains/ directory must produce an empty dict, not an exception."""
    reg = PoliciesRegistry()
    reg._domains_dir = Path("/nonexistent/path/domains")
    assert reg._load_domain_policies() == {}


def test_load_returns_empty_when_domain_has_no_policy_file(tmp_path):
    """Domains without a policy.py file are silently skipped."""
    (tmp_path / "games").mkdir()
    assert make_registry(tmp_path)._load_domain_policies() == {}


def test_load_skips_files_at_domains_root(tmp_path):
    """Regular files (e.g. __init__.py) at the domains/ root are not iterated."""
    (tmp_path / "__init__.py").write_text("")
    assert make_registry(tmp_path)._load_domain_policies() == {}


def test_load_discovers_valid_policy(tmp_path):
    """A well-formed domain policy is registered under its model name."""
    domain = tmp_path / "sample"
    domain.mkdir()
    (domain / "policy.py").touch()

    mod = fake_policy_module("domains.sample.policy", SamplePolicy)
    with patch("importlib.import_module", return_value=mod):
        result = make_registry(tmp_path)._load_domain_policies()

    assert "Sample" in result
    assert result["Sample"] is SamplePolicy


def test_load_excludes_base_policy_itself(tmp_path):
    """BasePolicy must not be registered even if re-exported from a domain module."""
    domain = tmp_path / "games"
    domain.mkdir()
    (domain / "policy.py").touch()

    mod = types.ModuleType("domains.games.policy")
    mod.BasePolicy = BasePolicy

    with patch("importlib.import_module", return_value=mod):
        result = make_registry(tmp_path)._load_domain_policies()

    assert "Base" not in result
    assert result == {}


def test_load_skips_non_class_attribute_ending_in_policy(tmp_path):
    """String or int attributes whose name ends in 'Policy' are ignored."""
    domain = tmp_path / "games"
    domain.mkdir()
    (domain / "policy.py").touch()

    mod = types.ModuleType("domains.games.policy")
    mod.GamePolicy = "not-a-class"

    with patch("importlib.import_module", return_value=mod):
        result = make_registry(tmp_path)._load_domain_policies()

    assert result == {}


def test_load_broken_import_logs_warning_and_continues(tmp_path, caplog, monkeypatch):
    """An ImportError in a domain policy logs a warning but does not crash."""
    monkeypatch.setattr(logging.getLogger("gameannouncer"), "propagate", True)
    domain = tmp_path / "broken"
    domain.mkdir()
    (domain / "policy.py").touch()

    with patch("importlib.import_module", side_effect=ImportError("oops")):
        with caplog.at_level(logging.WARNING):
            result = make_registry(tmp_path)._load_domain_policies()

    assert result == {}
    assert any("broken" in record.message for record in caplog.records)


def test_load_warns_on_key_collision(tmp_path, caplog, monkeypatch):
    """Registering two policies with the same model name logs a warning."""
    monkeypatch.setattr(logging.getLogger("gameannouncer"), "propagate", True)
    for name in ("alpha", "beta"):
        d = tmp_path / name
        d.mkdir()
        (d / "policy.py").touch()

    call_count = 0

    def fake_import(module_name: str) -> types.ModuleType:
        nonlocal call_count
        call_count += 1
        cls = SamplePolicy if call_count == 1 else OtherPolicy
        cls.__name__ = "SamplePolicy"
        return fake_policy_module(module_name, cls)

    with patch("importlib.import_module", side_effect=fake_import):
        with caplog.at_level(logging.WARNING):
            result = make_registry(tmp_path)._load_domain_policies()

    assert "Sample" in result
    assert any("Sample" in record.message for record in caplog.records)


def test_get_all_policies_result_is_cached(tmp_path):
    """Repeated calls to get_all_policies() return the identical dict object."""
    reg = make_registry(tmp_path)
    assert reg.get_all_policies() is reg.get_all_policies()


def test_clear_cache_resets_discovery(tmp_path):
    """After clear_cache(), the next call re-discovers policies from scratch."""
    reg = make_registry(tmp_path)
    reg.get_all_policies()
    reg.clear_cache()
    assert reg._cache is None
