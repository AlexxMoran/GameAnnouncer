# GameAnnouncer - AI Assistant Configuration

## Project Overview

**GameAnnouncer** is a full-stack web application for managing gaming events and announcements with user registration, authentication, and notifications.

### Technology Stack

**Backend:**
- FastAPI 0.117+ (async ASGI)
- Python 3.13+ with Uvicorn
- PostgreSQL + SQLAlchemy 2.0+ (async)
- JWT Authentication (fastapi-users)
- Taskiq + Redis (async task queue)
- Package Manager: UV

**Frontend:**
- React 19.2 + TypeScript 5.9
- Vite 7.2+
- MobX (NOT Redux)
- Material-UI v7.3+
- Axios
- Formik + Yup
- Emotion (CSS-in-JS) + SASS

**Note:** Ignore `frontend/` directory - Angular app being deprecated.

---

## Running Commands

**CRITICAL: This project uses UV as package manager. ALWAYS prefix Python commands with `uv run`:**

```bash
uv run pytest tests/
uv run alembic upgrade head
uv run python script.py
```

**Quick commands:**
- Tests: `uv run pytest` or `make test`
- Linters: `uv run ruff check .` or `make lint`
- Format: `uv run black .` or `make format`
- Dev server: `uv run uvicorn main:app --reload`

---

## Instructions for AI Assistant

**CRITICAL: When working on this project, ALWAYS follow this process:**

### 1. Determine Context

When the user asks you to work on a task, identify which part of the stack is involved:

- **Backend work** (API routes, database, services, Python files in `backend/`) → Read [docs/BACKEND.md](docs/BACKEND.md)
- **Frontend work** (React components, UI, TypeScript files in `frontend-react/`) → Read [docs/FRONTEND.md](docs/FRONTEND.md)

### 2. Load Required Documentation

**BEFORE writing any code**, use the Read tool to load the appropriate documentation file(s).

Example workflow:
```
User: "Add a new API endpoint for games"
Assistant: [Uses Read tool to read docs/BACKEND.md]
Assistant: [Follows backend guidelines from the documentation]
```

```
User: "Create a GameCard component"
Assistant: [Uses Read tool to read docs/FRONTEND.md]
Assistant: [Follows frontend guidelines from the documentation]
```

### 3. Follow Loaded Guidelines

Once you've read the appropriate documentation, follow ALL guidelines and patterns described there.

---

## Core Principles (Quick Reference)

### 1. Async-First Architecture
**ALWAYS use async/await for all I/O operations:**
- Database queries, HTTP requests, file operations, email sending, Redis operations
- Use `AsyncSession` for database
- Use Taskiq for background tasks

### 2. Strict Type Safety
**ALWAYS use type hints:**
- Python: Full type annotations for all parameters and returns
- TypeScript: Strict mode enabled, avoid `any`

### 3. Dependency Injection
- Use FastAPI `Depends()` for all dependencies
- Define reusable dependencies in `backend/core/deps.py`

### 4. Policy-Based Authorization
**NEVER hardcode permissions in routes:**
- Use `backend.core.permissions.facade` for all authorization
- Never check `user.id != resource.owner_id` directly in routes

### 5. Separation of Concerns

**Backend layers:**
1. Routes (`/api/`) - HTTP handling only
2. CRUD (`/api/v1/crud/`) - Database operations
3. Services (`/services/`) - Business logic
4. Models (`/models/`) - Database schema
5. Schemas (`/schemas/`) - Validation models

**Frontend layers:**
1. Pages (`/pages/`) - Route components
2. Features (`/features/`) - Feature components
3. Widgets (`/widgets/`) - Reusable UI
4. Services (`/shared/services/`) - State and API
5. UI (`/shared/ui/`) - Design system

---

## Critical Rules

### ALWAYS Do:
1. Use async/await for ALL I/O operations
2. Use full type hints (Python + TypeScript)
3. Use permission system for authorization (`facade.authorize_action()`)
4. Use SQLAlchemy 2.0 syntax (`session.execute()` + `select()`)
5. Use MobX for state management (NOT Redux)
6. Use Taskiq for background tasks (`.kiq()` method)
7. Validate all inputs (Pydantic, Yup)
8. Follow existing patterns in codebase
9. Use docstrings (Python) or JSDoc (TypeScript) for complex logic

### NEVER Do:
1. NEVER use sync I/O (blocking operations)
2. NEVER hardcode permissions in routes
3. NEVER commit secrets (use `.env`)
4. NEVER touch `frontend/` directory (deprecated Angular)
5. NEVER use Redux (use MobX)
6. NEVER use legacy SQLAlchemy 1.x API (`.query()`, `.filter()`)
7. NEVER mutate MobX state outside `runInAction()`
8. NEVER return raw SQLAlchemy models from routes (use Pydantic schemas)
9. NEVER use inline comments (`# comment` or `// comment`) - use docstrings/JSDoc instead
10. NEVER run Python commands without `uv run` prefix (e.g., use `uv run pytest`, NOT `pytest`)

---

## Security Essentials

- **Authentication:** Use `current_user` dependency, verify JWT on backend
- **Authorization:** Use permission system, never trust client data
- **Secrets:** NEVER commit to git, use environment variables
- **Input:** Validate ALL inputs with Pydantic (backend) and Yup (frontend)
- **SQL Injection:** Use parameterized queries (SQLAlchemy handles automatically)

---

## Code Style

**Backend (Python):**
- Formatter: Black (100 chars)
- Linter: Ruff
- Naming: `snake_case` (functions/vars), `PascalCase` (classes), `UPPER_CASE` (constants)
- **Documentation:** Use docstrings (`"""..."""`), NEVER inline comments (`# comment`)

**Frontend (TypeScript):**
- Linter: ESLint
- Naming: `camelCase` (functions/vars), `PascalCase` (components/types), `UPPER_CASE` (constants)
- **Documentation:** Use JSDoc comments (`/** ... */`), avoid inline comments

**Documentation Rules:**
- ❌ **NEVER** use inline comments (`# comment` or `// comment`)
- ✅ **ALWAYS** use docstrings (Python) or JSDoc (TypeScript) for complex logic
- Write self-documenting code with clear variable/function names

---

## Git Workflow

**Commits:** Use conventional commits
```
feat(module): description
fix(module): description
refactor(module): description
```

**Branches:**
- `feature/<name>` - new features
- `fix/<name>` - bug fixes
- `refactor/<name>` - refactoring

---

## Documentation Structure

- **[docs/BACKEND.md](docs/BACKEND.md)** - Detailed backend guidelines (Database, API, Services, Tasks, Testing)
- **[docs/FRONTEND.md](docs/FRONTEND.md)** - Detailed frontend guidelines (MobX, Components, Forms, Styling, Routing)

---

## Quick Start for AI

1. Read this file (CLAUDE.md) - you're doing it now
2. Identify if task is backend or frontend
3. Read appropriate docs/ file BEFORE coding
4. Follow all guidelines from the documentation
5. When in doubt, search codebase for similar implementations

**Remember:** The detailed guidelines in `docs/` override these quick reference rules if there's any conflict. Always load and follow the detailed documentation.
