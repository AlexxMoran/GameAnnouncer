# Backend Guidelines

This document contains detailed backend-specific guidelines for the GameAnnouncer project.

**Technology:** FastAPI 0.117+, Python 3.13+, PostgreSQL, SQLAlchemy 2.0+, Taskiq, Redis

---

## Database & SQLAlchemy

### Models

**Requirements:**
- Inherit from `Base` (provides `id`, `created_at`, `updated_at`)
- Use `Mapped[T]` type hints for all columns
- Define relationships with proper cascades
- Use `@validates` decorator for business rules validation

**Example structure:**
```python
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import String, DateTime, ForeignKey

class Announcement(Base):
    __tablename__ = "announcements"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    organizer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    organizer: Mapped["User"] = relationship("User")

    @validates("end_at")
    def validate_end_at(self, key: str, value: datetime) -> datetime:
        if self.start_at and value <= self.start_at:
            raise ValueError("end_at must be after start_at")
        return value
```

### Sessions

**CRITICAL: Use AsyncSession for all database operations**

- Get session from `get_async_session` dependency
- NEVER manually commit/rollback in routes (handled automatically)
- Use modern SQLAlchemy 2.0 syntax: `session.execute()` + `select()`
- NEVER use legacy 1.x API: `.query()`, `.filter()`, etc.

**GOOD - SQLAlchemy 2.0:**
```python
from sqlalchemy import select

async def get_game(game_id: int, session: AsyncSession) -> Game | None:
    result = await session.execute(
        select(Game).where(Game.id == game_id)
    )
    return result.scalar_one_or_none()
```

**BAD - legacy 1.x style:**
```python
# NEVER DO THIS
async def get_game(game_id: int, session: AsyncSession) -> Game | None:
    return await session.query(Game).filter(Game.id == game_id).first()
```

### Preventing N+1 Queries

Use `selectinload()` or `joinedload()` to eagerly load relationships:

```python
from sqlalchemy.orm import selectinload

result = await session.execute(
    select(Announcement)
    .options(selectinload(Announcement.organizer))
    .options(selectinload(Announcement.participants))
)
```

### Migrations

**ALWAYS create migrations for schema changes:**

1. Generate: `alembic revision --autogenerate -m "description"`
2. Review the generated migration file
3. Test: `alembic upgrade head` and `alembic downgrade -1`
4. NEVER edit merged migrations

---

## API Design

### Routes

**Naming conventions:**
- Version all APIs: `/api/v1/games`
- Follow REST conventions:
  - `GET /api/v1/games` - list all
  - `GET /api/v1/games/{id}` - get one
  - `POST /api/v1/games` - create
  - `PATCH /api/v1/games/{id}` - update
  - `DELETE /api/v1/games/{id}` - delete

### Request/Response

**Use Pydantic schemas from `/schemas/`:**
- Naming patterns: `*Create`, `*Update`, `*Response`, `*Filter`
- ALWAYS wrap responses in standardized formats:
  - Single resource: `DataResponse[T]` = `{"data": T}`
  - List: `PaginatedResponse[T]` = `{"data": [T], "skip": int, "limit": int, "total": int}`

**Route example:**
```python
from backend.schemas.base import DataResponse
from backend.schemas.game import GameCreate, GameResponse

@router.post("/games", response_model=DataResponse[GameResponse])
async def create_game(
    game_data: GameCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> DataResponse[GameResponse]:
    game = await GameCRUD.create(game_data, session, user)
    return DataResponse(data=GameResponse.model_validate(game))
```

### Dependencies

**Extract common dependencies to `backend/core/deps.py`:**

Use `Annotated` for clean, reusable dependency types:

```python
from typing import Annotated
from fastapi import Depends

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
UserDep = Annotated[User, Depends(current_user)]

@router.get("/games")
async def get_games(session: SessionDep, user: UserDep):
    pass
```

---

## Business Logic

### Services

**Location:** `/services/`

**Structure:**
- Services are stateless functions (not classes unless needed)
- Services orchestrate CRUD, permissions, and async tasks
- Services contain complex business logic

**Example:**
```python
# backend/services/create_announcement_service.py

async def create_announcement(
    data: AnnouncementCreate,
    user: User,
    session: AsyncSession,
) -> Announcement:
    # Validate dependencies
    game = await GameCRUD.get_by_id(data.game_id, session)
    if not game:
        raise NotFoundException("Game not found")

    # Create the resource
    announcement = await AnnouncementCRUD.create(data, session, user)

    # Trigger async task for notifications
    await send_announcement_notification.kiq(announcement.id)

    return announcement
```

---

## CRUD Pattern

**Location:** `/api/v1/crud/`

**Purpose:** Database operations only (no business logic)

**Structure:**
- Create, Read, Update, Delete operations
- Return SQLAlchemy models (convert to schemas in routes)
- Use `AsyncSession` for all operations

---

## Authorization

**CRITICAL: Use the permission system, NEVER hardcode authorization**

**GOOD - use permission system:**
```python
from backend.core.permissions import facade

async def update_game(game_id: int, user: User, session: AsyncSession):
    game = await GameCRUD.get_by_id(game_id, session)
    await facade.authorize_action("update", game, user)
    # Continue with update
```

**BAD - hardcoded permission logic:**
```python
# NEVER DO THIS
async def update_game(game_id: int, user: User, session: AsyncSession):
    game = await GameCRUD.get_by_id(game_id, session)
    if user.id != game.organizer_id and not user.is_superuser:
        raise HTTPException(403)
```

---

## Async Tasks

**Use Taskiq for all background work:**

**Location:** Define tasks in `/tasks/`

**Usage:**
- Use `.kiq()` method to enqueue tasks (non-blocking)
- NEVER block HTTP responses with slow operations

**GOOD - async task:**
```python
from backend.tasks.email_tasks import send_verification_email

async def register_user(data: UserCreate, session: AsyncSession) -> User:
    user = await UserCRUD.create(data, session)
    await send_verification_email.kiq(user.id)  # non-blocking
    return user
```

**BAD - blocks HTTP response:**
```python
# NEVER DO THIS
async def register_user(data: UserCreate, session: AsyncSession) -> User:
    user = await UserCRUD.create(data, session)
    await send_email_now(user.email)  # blocks the response
    return user
```

---

## Configuration

**Use Pydantic Settings in `backend/core/config.py`:**

- Store secrets in `.env` file (NEVER commit)
- Use nested config with double underscore: `DB__HOST`, `DB__PORT`
- Environment variables override default values

**Example:**
```python
from pydantic_settings import BaseSettings

class DatabaseConfig(BaseSettings):
    host: str = "localhost"
    port: int = 5432
    name: str = "gameannouncer"

class Settings(BaseSettings):
    db: DatabaseConfig = DatabaseConfig()

    class Config:
        env_nested_delimiter = "__"
```

---

## Testing

**Structure:** Mirror app structure in `/tests/`

**Tools:**
- `pytest` with `pytest-asyncio`
- `TestContainers` for integration tests
- `factory-boy` for test fixtures

**Example:**
```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_game(client: AsyncClient, auth_user):
    response = await client.post("/api/v1/games", json={
        "name": "Test Game",
        "description": "Test description",
    })
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "Test Game"
```

---

## Project Patterns

### Pagination

Backend provides `PaginatedResponse[T]`:
```python
{
    "data": [T],
    "skip": int,
    "limit": int,
    "total": int
}
```

### Search/Filtering

- Define search classes in `/searches/`
- Use Pydantic models for filter parameters
- Build queries dynamically based on provided filters

### Email

- MJML templates in `/mailers/`
- Send via async tasks (Taskiq)

### Scheduled Tasks

- Define in `/tasks/scheduler.py`
- Use Taskiq scheduler for cron jobs

---

## Performance Best Practices

1. **Indexing:** Index frequently queried columns
2. **Eager Loading:** Use `selectinload()` / `joinedload()` to prevent N+1 queries
3. **Pagination:** Always paginate large result sets
4. **Caching:** Use Redis for frequently accessed data
5. **Async Tasks:** Move slow operations (emails, reports) to background tasks
6. **SELECT specific columns:** Avoid `SELECT *` in queries

---

## What NOT to Do

1. **DO NOT** use synchronous I/O operations
2. **DO NOT** use legacy SQLAlchemy 1.x API (`.query()`, `.filter()`)
3. **DO NOT** commit secrets to git
4. **DO NOT** hardcode authorization logic
5. **DO NOT** block HTTP requests with slow operations
6. **DO NOT** return raw SQLAlchemy models from routes (use Pydantic schemas)
7. **DO NOT** edit merged migrations
8. **DO NOT** use `SELECT *` in queries
9. **DO NOT** manually commit/rollback in routes

---

## Development Workflow

1. **Before work:**
   - Pull latest from main
   - Create feature branch
   - Review related code

2. **During:**
   - Follow these guidelines
   - Write tests for new features
   - Run linters: `make lint`
   - Run tests: `make test`

3. **Before commit:**
   - Format code: `make format`
   - Fix linter errors
   - Ensure tests pass
   - Review your changes

---

## Additional Resources

- See [FRONTEND.md](FRONTEND.md) for frontend guidelines
- Main config: [CLAUDE.md](../CLAUDE.md)
