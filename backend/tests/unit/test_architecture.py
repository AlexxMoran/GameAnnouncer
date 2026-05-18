"""
Architecture guardrail tests.

These tests enforce layer boundaries that are easy to violate accidentally.
They parse import statements statically (no code execution) so they run
without a database and complete in milliseconds.

Invariants enforced:
- decisions.py in operations must be pure business rules (no SQLAlchemy, no FastAPI)
- modules must not import from operations (dependency direction: operations → modules, never the reverse)
- module service files must not import core.permissions (authorization belongs at entrypoints only)
- gateway.py in operations must cache loaded entities (load() sets self._<entity>, apply() uses assert)
"""

import ast
from pathlib import Path

BACKEND_DIR = Path(__file__).parent.parent.parent
OPERATIONS_DIR = BACKEND_DIR / "operations"
MODULES_DIR = BACKEND_DIR / "modules"


def _collect_imports(path: Path) -> list[str]:
    """Return all top-level module names imported by a Python source file."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    modules = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.append(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.append(node.module)
    return modules


def _find(directory: Path, filename: str) -> list[Path]:
    return list(directory.rglob(filename))


def test_decisions_do_not_import_sqlalchemy():
    """
    decisions.py must not depend on SQLAlchemy.

    The decisions layer contains pure business rules that operate on frozen
    dataclass snapshots. Importing SQLAlchemy would couple business logic to
    the persistence layer and break the ability to test decisions without a DB.
    """
    for path in _find(OPERATIONS_DIR, "decisions.py"):
        imports = _collect_imports(path)
        violations = [i for i in imports if i.startswith("sqlalchemy")]
        assert not violations, (
            f"{path.relative_to(BACKEND_DIR)}: decisions.py must not import SQLAlchemy, "
            f"found: {violations}"
        )


def test_decisions_do_not_import_fastapi():
    """
    decisions.py must not depend on FastAPI.

    HTTP status codes, request/response objects, and Depends() have no place
    in the business rule layer. A decisions class must be callable from any
    entrypoint: HTTP route, background task, CLI, or test.
    """
    for path in _find(OPERATIONS_DIR, "decisions.py"):
        imports = _collect_imports(path)
        violations = [i for i in imports if i.startswith("fastapi")]
        assert not violations, (
            f"{path.relative_to(BACKEND_DIR)}: decisions.py must not import FastAPI, "
            f"found: {violations}"
        )


def test_modules_do_not_import_operations():
    """
    Domain modules must not import from operations.

    The allowed dependency direction is: operations → modules (operations use
    domain code). The reverse creates circular architecture and prevents modules
    from being reused independently.
    """
    for path in MODULES_DIR.rglob("*.py"):
        imports = _collect_imports(path)
        violations = [i for i in imports if i.startswith("operations")]
        assert not violations, (
            f"{path.relative_to(BACKEND_DIR)}: module file must not import from operations, "
            f"found: {violations}"
        )


def test_module_services_do_not_import_permissions():
    """
    Module service files must not perform authorization.

    Authorization belongs exclusively at entrypoints (api/ routes and tasks/).
    Services are called after the entrypoint has already verified the user's
    rights. Importing core.permissions inside a service breaks this contract
    and makes services harder to reuse from system-triggered entrypoints.
    """
    for module_dir in MODULES_DIR.iterdir():
        services_dir = module_dir / "services"
        if not services_dir.is_dir():
            continue
        for path in services_dir.rglob("*.py"):
            imports = _collect_imports(path)
            violations = [i for i in imports if i.startswith("core.permissions")]
            assert not violations, (
                f"{path.relative_to(BACKEND_DIR)}: service must not import core.permissions, "
                f"found: {violations}"
            )


def _find_cache_attrs(cls: ast.ClassDef) -> set[str]:
    """
    Return self._xxx attributes declared as `self._xxx: T | None = None` in __init__.

    These are the gateway's cached-entity slots that load() is expected to fill.
    """
    init = next(
        (n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "__init__"),
        None,
    )
    if init is None:
        return set()

    cache_attrs: set[str] = set()
    for node in ast.walk(init):
        if not isinstance(node, ast.AnnAssign):
            continue
        target = node.target
        if not (
            isinstance(target, ast.Attribute)
            and isinstance(target.value, ast.Name)
            and target.value.id == "self"
            and target.attr.startswith("_")
            and not target.attr.startswith("__")
        ):
            continue
        if not (isinstance(node.value, ast.Constant) and node.value.value is None):
            continue
        if "None" not in ast.dump(node.annotation):
            continue
        cache_attrs.add(target.attr)

    return cache_attrs


def _asserted_self_attrs(method: ast.AsyncFunctionDef) -> set[str]:
    """Return self._xxx names referenced inside any assert statement in the method."""
    asserted: set[str] = set()
    for node in ast.walk(method):
        if not isinstance(node, ast.Assert):
            continue
        for inner in ast.walk(node.test):
            if (
                isinstance(inner, ast.Attribute)
                and isinstance(inner.value, ast.Name)
                and inner.value.id == "self"
            ):
                asserted.add(inner.attr)
    return asserted


def test_gateway_apply_uses_cached_entity():
    """
    gateway.py apply() must assert each entity cached by load().

    The pattern: load() stores the primary loaded entity on self
    (self._announcement: Announcement | None = None) and apply() guards access
    with assert self._announcement is not None before using it.

    This prevents redundant DB round-trips and makes the load() → apply()
    call order an explicit contract rather than a silent assumption.

    Detection: if __init__ declares self._x: T | None = None, apply() must
    reference self._x in at least one assert statement.
    """
    for path in _find(OPERATIONS_DIR, "gateway.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))

        for cls in ast.walk(tree):
            if not isinstance(cls, ast.ClassDef):
                continue

            cache_attrs = _find_cache_attrs(cls)
            if not cache_attrs:
                continue

            apply_method = next(
                (
                    node
                    for node in cls.body
                    if isinstance(node, ast.AsyncFunctionDef) and node.name == "apply"
                ),
                None,
            )
            if apply_method is None:
                continue

            asserted = _asserted_self_attrs(apply_method)
            missing = cache_attrs - asserted
            assert not missing, (
                f"{path.relative_to(BACKEND_DIR)}: {cls.name}.apply() declares "
                f"cached attributes {missing} in __init__ but does not assert them — "
                f"add `assert self.{next(iter(missing))} is not None` at the top of apply()."
            )
