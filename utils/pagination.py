# stdlib
from math import ceil
from typing import Any


class Pagination:
    def __init__(self, page: int, pages: int, on_page: int, results: int) -> None:
        self.page = page
        self.pages = pages
        self.on_page = on_page
        self.results = results


# TODO: fixme
def get_pagination(page: int, limit: int, count: int) -> dict[str, Any]:
    try:
        pages = ceil(count / limit)
    except Exception:
        pages = 0
        count = 0

    pagination = Pagination(
        page=page,
        pages=pages,
        on_page=limit,
        results=count,
    )
    return pagination.__dict__
