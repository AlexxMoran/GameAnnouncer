from types import SimpleNamespace
from sqlalchemy import String
from searches.base_search import BaseSearch


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
