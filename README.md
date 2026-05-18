# GameAnnouncer

GameAnnouncer is a platform for managing gaming events — creating announcements, handling participant registration, running qualification rounds, generating tournament brackets, and recording match results.

---

## Technology Stack

**Backend**
- Python 3.13 · FastAPI 0.117+ · SQLAlchemy 2.0 async · Alembic
- Authentication: fastapi-users (JWT)
- Task queue: Taskiq + Redis
- Database: PostgreSQL
- Package manager: UV

**Frontend** *(active)*
- React 19 · TypeScript 5 · Vite · MobX · Material UI v7

**Frontend** *(deprecated)*
- Angular app in `frontend/` — being phased out, ignore for new development

**Tooling**
- Formatter: Black · Linter: Ruff
- Tests: pytest + pytest-asyncio + testcontainers
- Containers: Docker Compose

---

## Architecture

The backend follows a **layered operation-oriented architecture**. Each layer has a single responsibility and strict import rules.

```
api/          HTTP interface — routes, auth guards, request/response schemas
operations/   Complex multi-step business operations (see below)
modules/      Domain layer — models, repositories, state machines, simple services
core/         Platform support — config, permissions, DI, middleware
tasks/        Background and scheduled entrypoints
```

### Operation-Oriented Approach

Meaningful multi-step business behavior lives in `operations/{verb_object}/` rather than in large service files. Each operation is a self-contained folder:

```
operations/generate_announcement_bracket/
  contract.py    — input definition (Pydantic, no framework knowledge)
  scenario.py    — orchestration: load → decide → apply
  gateway.py     — DB reads and writes, ORM ↔ operation data translation
  structures.py  — frozen dataclasses: Snapshot (facts) and Decision (plan)
  decisions.py   — pure business rules, no I/O, testable without a database
  README.md      — invariants, reads, writes, danger zones (on risky operations)
```

Data flow:
```
Contract → Scenario → Gateway.load() → Snapshot → Decisions.make() → Decision → Gateway.apply() → Result
```

**Layer rules (enforced by `tests/unit/test_architecture.py`):**
- `decisions.py` must not import SQLAlchemy or FastAPI
- `modules/` must not import from `operations/`
- Module service files must not import `core.permissions`
- `gateway.apply()` must use entities cached by `gateway.load()`, not re-query the DB

Simple CRUD, searches, and single-step updates stay inside `modules/`.

---

## Project Structure

```
GameAnnouncer/
├── backend/
│   ├── api/v1/                   # Route handlers (HTTP + auth only)
│   ├── operations/               # Complex business operations
│   │   ├── create_announcement/
│   │   ├── update_announcement/
│   │   ├── create_registration_request/
│   │   ├── change_registration_request_status/
│   │   ├── finalize_announcement_qualification/
│   │   ├── generate_announcement_bracket/
│   │   └── submit_match_result/
│   ├── modules/                  # Domain models, repos, state machines
│   │   ├── announcements/
│   │   ├── matches/
│   │   ├── participants/
│   │   ├── registration/
│   │   ├── games/
│   │   └── users/
│   ├── core/                     # Config, DI, permissions facade, middleware
│   ├── tasks/                    # Background tasks (Taskiq)
│   ├── tests/                    # Test suite (mirrors backend structure)
│   │   └── unit/test_architecture.py  # Layer boundary guardrails
│   ├── alembic/                  # DB migrations
│   ├── main.py                   # ASGI entrypoint
│   └── pyproject.toml
├── react-frontend/               # Active React frontend
├── frontend/                     # Angular app (deprecated)
├── docs/
│   ├── BACKEND.md
│   ├── FRONTEND.md
│   └── operation-oriented-architecture.md
├── docker-compose.yml
└── Makefile
```

---

## Quick Start

1. Copy the environment template:

```bash
cp backend/.env.template backend/.env
# Fill in DB credentials, Redis URL, secrets, etc.
```

2. Start all services:

```bash
make project-up
```

This brings up PostgreSQL, Redis, Mailpit, the backend API, the React frontend, and the Taskiq worker.

---

## Running Backend Commands

This project uses **UV** as the package manager. Always prefix Python commands with `uv run`:

```bash
uv run pytest                          # run all tests
uv run pytest tests/unit/ -v           # architecture guardrails only
uv run ruff check .                    # lint
uv run black .                         # format
uv run alembic upgrade head            # apply migrations
```

Or via Make shortcuts:

```bash
make test
make lint
make format
```

---

## Local URLs

| Service | URL |
|---|---|
| React frontend | http://localhost:5173 |
| API | http://localhost:3000 |
| API docs (Swagger) | http://localhost:3000/docs |
| Mailpit (email UI) | http://localhost:8025 |

Check `docker-compose.yml` if ports differ.

---

## Developer Docs

- [docs/BACKEND.md](docs/BACKEND.md) — backend guidelines, patterns, conventions
- [docs/FRONTEND.md](docs/FRONTEND.md) — frontend guidelines (React/MobX)
- [docs/operation-oriented-architecture.md](docs/operation-oriented-architecture.md) — full operation pattern reference

---

## License

MIT — see `LICENSE`.
