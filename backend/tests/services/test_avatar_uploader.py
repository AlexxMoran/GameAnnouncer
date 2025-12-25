import pytest
from types import SimpleNamespace
from exceptions.app_exception import AppException


import services.avatar_uploader as au


class FakeUpload(SimpleNamespace):
    async def read(self, n=-1):
        return b"data"


@pytest.mark.asyncio
async def test_upload_avatar_invalid_extension():
    f = SimpleNamespace(filename="file.txt", read=FakeUpload().read)
    with pytest.raises(AppException):
        await au.upload_avatar("user", 1, f)


@pytest.mark.asyncio
async def test_upload_avatar_writes_file(monkeypatch, tmp_path):
    f = SimpleNamespace(filename="file.png")
    chunks = [b"x", b""]

    async def fake_read(n=-1):
        try:
            return chunks.pop(0)
        except IndexError:
            return b""

    f.read = fake_read

    monkeypatch.setattr(au, "BASE_DIR", str(tmp_path))
    monkeypatch.setattr("uuid.uuid4", lambda: SimpleNamespace(hex="deadbeef"))

    res = await au.upload_avatar("user", 2, f)
    assert res.startswith("/")
