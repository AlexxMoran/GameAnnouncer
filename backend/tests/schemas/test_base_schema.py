from schemas.base import DataResponse, PaginatedResponse


def test_data_and_paginated_response_containers():
    dr = DataResponse[_data := int](data=5)
    assert dr.data == 5
    pr = PaginatedResponse[_data := int](data=[1, 2], skip=0, limit=10, total=2)
    assert pr.total == 2
