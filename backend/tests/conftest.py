import os
import asyncio
import importlib

import pytest
import pytest_asyncio
import httpx

from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncConnection,
    async_sessionmaker,
)

from models import Base
from core.db import database as core_db_mod


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def engine():
    """Create a test engine for the whole test session and create all tables once."""
    TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    engine = create_async_engine(TEST_DATABASE_URL, future=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def connection(engine: create_async_engine):
    """Create a connection that stays open for the whole test session.

    Each test will begin a nested transaction (SAVEPOINT) on this connection and roll it back,
    giving fast isolated tests.
    """
    async with engine.connect() as conn:
        await conn.begin()
        yield conn
        await conn.rollback()


@pytest_asyncio.fixture
async def db_session(connection: AsyncConnection):
    """Yields a SQLAlchemy `AsyncSession` bound to a nested transaction for each test.

    This follows SQLAlchemy testing recommendations: begin a SAVEPOINT per test and
    listen for `after_transaction_end` to restart nested transactions when needed.
    """

    AsyncSessionLocal = async_sessionmaker(bind=connection, expire_on_commit=False)

    async with connection.begin_nested():
        async with AsyncSessionLocal() as session:

            @event.listens_for(session.sync_session, "after_transaction_end")
            def restart_savepoint(sess, transaction):
                if not sess.is_active:
                    sess.begin_nested()

            yield session


@pytest_asyncio.fixture
async def async_client(db_session, monkeypatch):
    """Return an `httpx.AsyncClient` for the FastAPI app using a per-test DB session.

    This fixture overrides the application's `db.session_getter` dependency so routes
    receive the `db_session` provided by the test.
    """
    monkeypatch.setattr("core.initializers.initialize_all", lambda: None)

    async def _noop_async():
        return None

    monkeypatch.setattr("tasks.broker.startup_broker", _noop_async)
    monkeypatch.setattr("tasks.broker.shutdown_broker", _noop_async)

    main = importlib.import_module("main")
    app = getattr(main, "app")

    async def _override_session_getter():
        yield db_session

    app.dependency_overrides[core_db_mod.db.session_getter] = _override_session_getter

    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
