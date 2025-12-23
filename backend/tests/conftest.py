import importlib
import os
from pathlib import Path
from typing import AsyncGenerator, Generator

import httpx
import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from testcontainers.postgres import PostgresContainer
from core.config import get_settings
from core.db.container import db


@pytest.fixture(scope="session")
def postgres_container() -> Generator[PostgresContainer, None, None]:
    """Start a temporary Postgres container for the test session.

    Requires Docker.
    """
    with PostgresContainer(
        image="postgres:15",
        username="test",
        password="test",
        dbname="test",
    ) as postgres:
        yield postgres


@pytest.fixture(scope="session")
def sync_db_url(postgres_container) -> str:
    """Return sync SQLAlchemy connection URL from the Postgres container."""

    return postgres_container.get_connection_url()


@pytest.fixture(scope="session")
def async_db_url(sync_db_url) -> str:
    """Derive an async (asyncpg) DB URL from the provided sync URL."""

    if "asyncpg" in sync_db_url:
        return sync_db_url

    if "postgresql+psycopg2" in sync_db_url:
        return sync_db_url.replace("postgresql+psycopg2", "postgresql+asyncpg")

    if sync_db_url.startswith("postgresql://"):
        return sync_db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

    return sync_db_url


@pytest.fixture(scope="session")
def migrated_db(sync_db_url) -> str:
    """Run Alembic migrations against the sync DB and return the URL."""

    os.environ["DATABASE_SYNC_URL"] = sync_db_url

    alembic_ini_path = Path(__file__).resolve().parents[1] / "alembic.ini"
    alembic_cfg = Config(str(alembic_ini_path))

    command.upgrade(alembic_cfg, "head")

    return sync_db_url


@pytest_asyncio.fixture(scope="function")
async def engine(migrated_db, async_db_url) -> AsyncGenerator[AsyncEngine, None]:
    """Create and yield an async SQLAlchemy engine for a test.

    Engine is disposed after the test.
    """

    engine = create_async_engine(async_db_url, echo=False)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def connection(engine) -> AsyncGenerator[AsyncConnection, None]:
    """Open a connection and start a transaction; rollback after test."""

    async with engine.connect() as conn:
        await conn.begin()
        yield conn
        await conn.rollback()


@pytest_asyncio.fixture
async def db_session(connection: AsyncConnection) -> AsyncGenerator[AsyncSession, None]:
    """Provide an async DB session inside a nested transaction (savepoint).

    Session is yielded and rolled back after the test.
    """

    SessionLocal = async_sessionmaker(
        bind=connection,
        expire_on_commit=False,
    )

    async with connection.begin_nested():
        async with SessionLocal() as session:

            @event.listens_for(session.sync_session, "after_transaction_end")
            def restart_savepoint(sess, transaction):
                if not sess.is_active:
                    sess.begin_nested()

            yield session


@pytest.fixture(scope="function")
def app(async_db_url, sync_db_url, monkeypatch):
    """Import FastAPI app with startup tasks disabled for testing."""

    get_settings.cache_clear()

    os.environ["DATABASE_URL"] = async_db_url
    os.environ["DATABASE_SYNC_URL"] = sync_db_url

    monkeypatch.setattr("core.initializers.initialize_all", lambda: None)

    async def _noop():
        return None

    monkeypatch.setattr("tasks.broker.startup_broker", _noop)
    monkeypatch.setattr("tasks.broker.shutdown_broker", _noop)

    main = importlib.import_module("main")

    return main.app


@pytest_asyncio.fixture
async def async_client(app, db_session) -> AsyncGenerator[httpx.AsyncClient, None]:
    """Provide an httpx AsyncClient wired to the app and test DB session."""

    async def override_session_getter():
        yield db_session

    app.dependency_overrides[db.session_getter] = override_session_getter

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
