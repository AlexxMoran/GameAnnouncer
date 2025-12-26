import importlib
import os
import core.config as config
import httpx
import pytest
import pytest_asyncio

from pathlib import Path
from typing import AsyncGenerator, Generator
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

pytest_plugins = ["tests.factory_fixtures"]


def test_settings(sync_db_url: str) -> config.Settings:
    """Build a minimal `Settings` instance for tests.

    Returns a `Settings` object constructed from the provided sync
    database URL and lightweight auth defaults. Tests will monkeypatch
    `core.config.get_settings` to return this instance.
    """

    from urllib.parse import urlparse

    parsed = urlparse(sync_db_url)

    settings_data = {
        "db": {
            "server": parsed.hostname or "localhost",
            "port": parsed.port or 5432,
            "user": parsed.username or "test",
            "password": parsed.password or "test",
            "database": (parsed.path or "").lstrip("/") or "test",
            "echo": False,
        },
        "auth": {
            "secret_key": "test-secret",
            "refresh_secret_key": "test-refresh",
            "verification_token_secret": "test-verify",
            "reset_password_token_secret": "test-reset",
        },
    }

    return config.Settings(**settings_data)


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

    url = postgres_container.get_connection_url()

    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)

    if "postgresql+psycopg2" in url:
        return url.replace("postgresql+psycopg2", "postgresql+psycopg")

    return url


@pytest.fixture(scope="session")
def async_db_url(sync_db_url) -> str:
    """Derive an async (asyncpg) DB URL from the provided sync URL."""

    if "asyncpg" in sync_db_url:
        return sync_db_url

    if "postgresql+psycopg" in sync_db_url:
        return sync_db_url.replace("postgresql+psycopg", "postgresql+asyncpg")

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

    settings_instance = test_settings(sync_db_url)

    monkeypatch.setattr(config, "get_settings", lambda: settings_instance)
    monkeypatch.setattr("core.db.container.get_settings", lambda: settings_instance)
    monkeypatch.setattr("core.initializers.initialize_all", lambda: None)

    async def _noop():
        return None

    monkeypatch.setattr("tasks.broker.startup_broker", _noop)
    monkeypatch.setattr("tasks.broker.shutdown_broker", _noop)

    try:
        from tasks.email_tasks import (
            send_verification_email_task,
            send_password_reset_email_task,
        )

        async def _noop_task(*args, **kwargs):
            return None

        setattr(send_verification_email_task, "kiq", _noop_task)
        setattr(send_password_reset_email_task, "kiq", _noop_task)
    except Exception:
        pass

    main = importlib.import_module("main")

    return main.app


@pytest_asyncio.fixture
async def async_client(app, db_session) -> AsyncGenerator[httpx.AsyncClient, None]:
    """Provide an httpx AsyncClient wired to the app and test DB session."""
    from core import deps as core_deps

    async def override_session_getter():
        yield db_session

    app.dependency_overrides[core_deps._session_getter_dep] = override_session_getter

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
def authenticated_client(async_client):
    """Return a client fixture that can be authenticated with a user."""

    def _authenticated_client(user):
        async def _current_user():
            return user

        import core.users as users_mod

        async_client._transport.app.dependency_overrides[users_mod.current_user] = (
            _current_user
        )
        return async_client

    return _authenticated_client
