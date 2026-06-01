from dataclasses import dataclass, field
from itertools import batched
from typing import Iterable, TypeAlias, Self

SomeRemoteData: TypeAlias = int


@dataclass
class Query:
    per_page: int = 3
    page: int = 1


@dataclass
class Page:
    per_page: int = 3
    results: Iterable[SomeRemoteData] = field(default_factory=list)
    next: int | None = None


def request(query: Query) -> Page:
    data = [i for i in range(0, 10)]
    chunks = list(batched(data, query.per_page))
    return Page(
        per_page=query.per_page,
        results=chunks[query.page - 1],
        next=query.page + 1 if query.page < len(chunks) else None,
    )


class RetrieveRemoteData:
    def __init__(self, per_page: int) -> None:
        self.per_page = per_page
        self.start_page = 1

    def __iter__(self):
        page_count = self.start_page
        while True:
            page = request(Query(per_page=self.per_page, page=page_count))
            yield from page.results
            if page.next is None:
                break
            page_count += 1


class Fibo:
    def __init__(self, n: int) -> None:
        self.n = n
        self.prev: int = 0
        self.next: int = 1
        self.counter: int = 0

    def __next__(self):
        if self.counter >= self.n:
            raise StopIteration

        curr = self.prev
        self.prev, self.next = self.next, self.next + self.prev

        self.counter += 1

        return curr

    def __iter__(self) -> Self:
        return self
