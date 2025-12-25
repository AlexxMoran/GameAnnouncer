from schemas.filters.base_filter import BaseFilter


def test_base_filter_values_excludes_none_and_includes_values():
    class MyFilter(BaseFilter):
        a: int | None = None
        b: str | None = None

    f = MyFilter()
    assert f.values() == {}

    f2 = MyFilter(a=1, b=None)
    assert f2.values() == {"a": 1}
