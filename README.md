# 🎮 GameAnnouncer

GameAnnouncer is an internal platform for publishing game announcements and managing gaming events.

In short: a full-stack web application with a FastAPI backend and an Angular frontend for creating games, posting announcements, managing registrations, and sending notifications.

---

## Technology Stack

- Backend: Python, FastAPI, SQLAlchemy (async), Alembic
- Configuration and validation: pydantic v2 / pydantic-settings
- Authentication: fastapi-users
- Task queue / worker: Taskiq
- Database: PostgreSQL
- Testing: pytest, testcontainers
- Containerization: Docker, Docker Compose
- Frontend: Angular, TypeScript

---

## Project Structure (top-level)

```
GameAnnouncer/
├── backend/           # FastAPI backend (API, models, migrations)
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── alembic/
├── frontend/          # Angular application
├── docker-compose.yml # Docker Compose configuration
└── Makefile           # Development helpers (start, build, logs)
```

---

## Quick Start for New Developers

1. Copy the backend environment template and fill in environment-specific values:

```bash
cp backend/.env.template backend/.env
# Edit backend/.env (DB credentials, hostnames, secrets, etc.)
```

2. Bring up all services from the repository root:

```bash
make project-up
```

This will start the required containers: PostgreSQL, Redis, Mailpit, backend, frontend and worker.

---

## Default local URLs

- Frontend: http://localhost:4200
- API: http://localhost:3000
- API Docs (Swagger): http://localhost:3000/docs
- Mail UI (Mailpit): http://localhost:8025
- PgAdmin (if enabled): http://localhost:5050

Check `docker-compose.yml` and `backend/.env` if ports have been changed.

---

## License

This project is licensed under the MIT License — see the `LICENSE` file.

---

If you like, I can add an instruction for rebuilding only the frontend container (e.g. `docker compose up -d --build frontend`) or add a section about running the backend locally without Docker.



