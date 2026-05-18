# AGENTS.md

Repository guidance for Codex and other coding agents.

## Start Here

- For backend work, read `docs/BACKEND.md` before editing code.
- For complex backend business behavior, also read `docs/operation-oriented-architecture.md`.
- For frontend work, read `docs/FRONTEND.md` before editing code.
- Prefer existing project patterns over inventing new abstractions.

## Backend Architecture

- Simple CRUD, search, and one-step behavior should stay in `backend/modules/**`, routes, or repositories.
- Meaningful multi-step business behavior should live in `backend/operations/{verb_object}/`.
- Operation structure:

```text
contract.py
scenario.py
gateway.py
structures.py
decisions.py
```

- Operation flow:

```text
Contract -> Scenario -> Gateway.load -> Snapshot -> Decisions -> Decision -> Gateway.apply -> Result
```

- `scenario.py` orders steps.
- `gateway.py` translates between ORM/project modules and operation structures.
- `structures.py` stores internal snapshots, decisions, and small value objects.
- `decisions.py` contains business rules and should not depend on ORM/framework objects.
- Keep authorization in API/task/webhook entrypoints unless the project explicitly changes that model.

## Commands

Run backend commands from `backend/` and prefix Python commands with `uv run`:

```bash
uv run pytest
uv run ruff check .
uv run alembic upgrade head
```

Focused examples:

```bash
uv run pytest tests/operations/generate_announcement_bracket -q
uv run pytest tests/api/v1/test_announcements.py -q
uv run ruff check operations api/v1/announcements.py
```

## Change Discipline

- Do not revert unrelated user changes.
- Keep edits scoped to the requested behavior.
- Add or update tests when changing behavior.
- For operation changes, prefer both pure `decisions.py` tests and scenario/integration tests when practical.
- After moving files or changing imports, run focused tests and `ruff check` on affected paths.

## Useful Docs

- `docs/BACKEND.md`
- `docs/FRONTEND.md`
- `docs/operation-oriented-architecture.md`
