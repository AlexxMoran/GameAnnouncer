from types import SimpleNamespace
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import String

from core.search.base_search import BaseSearch
from enums.registration_status import RegistrationStatus


class FakeColumn:
    def __init__(self, typ):
        self.type = typ

    def ilike(self, pattern):
        return ("ilike", pattern)

    def __eq__(self, other):
        return ("eq", other)


class DummyQuery:
    def __init__(self):
        self.conditions = []

    def where(self, cond):
        self.conditions.append(cond)
        return self


def test_apply_filters_string_and_non_string_and_handler():
    class S(BaseSearch):
        model = SimpleNamespace(
            name=FakeColumn(String()), category=FakeColumn(object())
        )

        def filter_by_special(self, query, value):
            return query.where(("handled", value))

    filters = SimpleNamespace(
        model_dump=lambda exclude_none=True: {
            "name": "foo",
            "category": 2,
            "special": "x",
        }
    )
    s = S(session=None, filters=filters)
    q = DummyQuery()
    q = s.apply_filters(q)
    assert ("ilike", "%foo%") in q.conditions
    assert ("eq", 2) in q.conditions
    assert ("handled", "x") in q.conditions


def test_apply_filters_native_enum_uses_exact_match_by_value():
    class S(BaseSearch):
        model = SimpleNamespace(status=FakeColumn(SQLEnum(RegistrationStatus)))

    filters = SimpleNamespace(
        model_dump=lambda exclude_none=True: {"status": RegistrationStatus.PENDING}
    )
    s = S(session=None, filters=filters)
    q = DummyQuery()

    q = s.apply_filters(q)

    assert ("eq", "pending") in q.conditions
    assert not any(condition[0] == "ilike" for condition in q.conditions)
