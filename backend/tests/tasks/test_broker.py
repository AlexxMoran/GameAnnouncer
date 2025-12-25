import pytest
from unittest.mock import AsyncMock

import tasks.broker as tb


@pytest.mark.asyncio
async def test_startup_broker_starts_when_not_worker():
    tb.broker.is_worker_process = False
    tb.broker.startup = AsyncMock()
    await tb.startup_broker()
    tb.broker.startup.assert_awaited_once()


@pytest.mark.asyncio
async def test_startup_broker_skips_when_worker():
    tb.broker.is_worker_process = True
    tb.broker.startup = AsyncMock()
    await tb.startup_broker()
    tb.broker.startup.assert_not_awaited()


@pytest.mark.asyncio
async def test_shutdown_broker_shuts_when_not_worker():
    tb.broker.is_worker_process = False
    tb.broker.shutdown = AsyncMock()
    await tb.shutdown_broker()
    tb.broker.shutdown.assert_awaited_once()


@pytest.mark.asyncio
async def test_shutdown_broker_skips_when_worker():
    tb.broker.is_worker_process = True
    tb.broker.shutdown = AsyncMock()
    await tb.shutdown_broker()
    tb.broker.shutdown.assert_not_awaited()
