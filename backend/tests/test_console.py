import pytest
import sys
import console
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock


def setup_db_mocks():
    session = SimpleNamespace()
    console.db.get_session = AsyncMock(return_value=session)
    console.db.dispose = AsyncMock()
    return session


@pytest.mark.asyncio
async def test_main_uses_ipython():
    from unittest.mock import patch

    setup_db_mocks()

    ipy = SimpleNamespace(start_ipython=Mock())
    nest = SimpleNamespace(apply=Mock())

    with patch.dict(sys.modules, {"IPython": ipy, "nest_asyncio": nest}):
        await console.main()

    ipy.start_ipython.assert_called_once()
    console.db.dispose.assert_awaited()


@pytest.mark.asyncio
async def test_main_falls_back_to_code_interact():
    from unittest.mock import patch
    import builtins
    import code as _code

    setup_db_mocks()

    orig_interact = _code.interact
    mock_interact = Mock()
    _code.interact = mock_interact

    real_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name.startswith("IPython") or name.startswith("nest_asyncio"):
            raise ImportError()
        return real_import(name, globals, locals, fromlist, level)

    with patch("builtins.__import__", side_effect=fake_import):
        try:
            await console.main()
        finally:
            _code.interact = orig_interact

    assert mock_interact.called
    console.db.dispose.assert_awaited()
