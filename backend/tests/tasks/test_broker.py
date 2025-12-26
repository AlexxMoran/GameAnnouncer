import pytest
from unittest.mock import AsyncMock, MagicMock, patch

import tasks.broker as tb


@pytest.mark.asyncio
async def test_startup_broker_starts_when_not_worker():
    mock_broker = MagicMock()
    mock_broker.is_worker_process = False
    mock_broker.startup = AsyncMock()
    with patch.object(tb, "get_broker", return_value=mock_broker):
        await tb.startup_broker()
    mock_broker.startup.assert_awaited_once()


@pytest.mark.asyncio
async def test_startup_broker_skips_when_worker():
    mock_broker = MagicMock()
    mock_broker.is_worker_process = True
    mock_broker.startup = AsyncMock()
    with patch.object(tb, "get_broker", return_value=mock_broker):
        await tb.startup_broker()
    mock_broker.startup.assert_not_awaited()


@pytest.mark.asyncio
async def test_shutdown_broker_shuts_when_not_worker():
    mock_broker = MagicMock()
    mock_broker.is_worker_process = False
    mock_broker.shutdown = AsyncMock()
    with patch.object(tb, "get_broker", return_value=mock_broker):
        await tb.shutdown_broker()
    mock_broker.shutdown.assert_awaited_once()


@pytest.mark.asyncio
async def test_shutdown_broker_skips_when_worker():
    mock_broker = MagicMock()
    mock_broker.is_worker_process = True
    mock_broker.shutdown = AsyncMock()
    with patch.object(tb, "get_broker", return_value=mock_broker):
        await tb.shutdown_broker()
    mock_broker.shutdown.assert_not_awaited()
