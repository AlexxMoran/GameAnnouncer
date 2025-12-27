import json
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from jwt import ExpiredSignatureError
from sqlalchemy.exc import IntegrityError, DataError

from exceptions.exception_handler import (
    _extract_regex,
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    database_exception_handler,
    generic_exception_handler,
)
from exceptions.app_exception import AppException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


def make_request(method="GET", path="/test", headers=None):
    return SimpleNamespace(
        method=method, url=SimpleNamespace(path=path), headers=headers or {}
    )


def test_extract_regex_basic():
    text = "Key (email)=(user@example.com)"
    pattern = r"Key\s*\(([^)]+)\)=\(([^)]+)\)"
    assert _extract_regex(pattern, text, group=1) == "email"
    assert _extract_regex(pattern, text, group=2) == "user@example.com"
    assert _extract_regex(pattern, "no match here") is None


@pytest.mark.asyncio
async def test_app_exception_handler_returns_correct_json():
    req = make_request("POST", "/resource")
    exc = AppException("oops", status_code=418, error_type="test", error={"a": 1})
    resp = await app_exception_handler(req, exc)
    assert resp.status_code == 418
    body = json.loads(resp.body)
    assert body["detail"] == "oops"
    assert body["error_type"] == "test"
    assert body["error"] == {"a": 1}


@pytest.mark.asyncio
async def test_http_exception_handler_missing_and_invalid_token():
    req = make_request("GET", "/x", headers={})
    exc = StarletteHTTPException(status_code=401, detail="Auth required")
    resp = await http_exception_handler(req, exc)
    assert resp.status_code == 401
    body = json.loads(resp.body)
    assert body["error_type"] == "missing_token"

    req2 = make_request("GET", "/x", headers={"authorization": "Bearer tok"})
    exc2 = StarletteHTTPException(status_code=401, detail="Auth required")
    with patch(
        "exceptions.exception_handler.jwt.decode", side_effect=ExpiredSignatureError()
    ):
        resp2 = await http_exception_handler(req2, exc2)
    assert resp2.status_code == 401
    body2 = json.loads(resp2.body)
    assert body2["error_type"] == "token_expired"


@pytest.mark.asyncio
async def test_validation_exception_handler_formats_errors():
    req = make_request("POST", "/create")
    errors = [
        {"loc": ("body", "name"), "msg": "field required"},
        {"loc": ("body", "age"), "msg": "value is not a valid integer"},
    ]
    exc = RequestValidationError(errors)
    resp = await validation_exception_handler(req, exc)
    assert resp.status_code == 422
    body = json.loads(resp.body)
    assert "name: field required" in body["detail"]
    assert "age: value is not a valid integer" in body["detail"]


@pytest.mark.asyncio
async def test_database_exception_handler_integrity_and_data_error():
    req = make_request("POST", "/db")

    orig = Exception(
        "duplicate key value violates unique constraint Key (email)=(x@example.com)"
    )
    ie = IntegrityError("", {}, orig)
    resp = await database_exception_handler(req, ie)
    assert resp.status_code == 409
    body = json.loads(resp.body)
    assert "email" in body["detail"]

    de = DataError("", {}, Exception("invalid input syntax for type integer"))
    resp2 = await database_exception_handler(req, de)
    assert resp2.status_code == 400
    body2 = json.loads(resp2.body)
    assert "Invalid data format" in body2["detail"]


@pytest.mark.asyncio
async def test_generic_exception_handler_returns_500():
    req = make_request("GET", "/boom")
    resp = await generic_exception_handler(req, Exception("uh oh"))
    assert resp.status_code == 500
    body = json.loads(resp.body)
    assert body["detail"] == "An unexpected error occurred"
