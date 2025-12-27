import pytest

from types import SimpleNamespace
from unittest.mock import AsyncMock
from searches.game_search import GameSearch


class ChainQuery:
    def outerjoin(self, *a, **k):
        return self

    def add_columns(self, *a, **k):
        return self

    def group_by(self, *a, **k):
        return self

    def offset(self, *a, **k):
        return self

    def limit(self, *a, **k):
        return self

    def order_by(self, *a, **k):
        return self


@pytest.mark.asyncio
async def test_results_with_announcements_count_sets_attribute():
    fake_session = SimpleNamespace()
    g1 = SimpleNamespace(id=1)
    g2 = SimpleNamespace(id=2)
    result = SimpleNamespace(all=lambda: [(g1, 3), (g2, 0)])
    fake_session.execute = AsyncMock(return_value=result)

    filters = SimpleNamespace(model_dump=lambda exclude_none=True: {})
    gs = GameSearch(session=fake_session, filters=filters)
    gs.base_query = lambda: ChainQuery()

    out = await gs.results_with_announcements_count()
    assert len(out) == 2
    assert hasattr(out[0], "announcements_count") and out[0].announcements_count == 3
    assert out[1].announcements_count == 0
