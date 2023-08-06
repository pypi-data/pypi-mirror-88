from __future__ import annotations

import logging
from dataclasses import dataclass, field
from logging import Logger
from typing import Any, AsyncIterable, Iterable, Iterator, Callable

from robot.api import Collector, Context
from robot.api import X

__logger__ = logging.getLogger(__name__)


class AsyncIterableAdapter():
    iterator: Iterator[X]

    def __init__(self, iterable: Iterable[X]):
        self.iterator = iter(iterable)

    async def __anext__(self):
        try:
            return next(self.iterator)
        except StopIteration:
            raise StopAsyncIteration

    def __aiter__(self) -> 'self':
        return self


@dataclass()
class PagesUrlCollector(Collector[X, AsyncIterable[str]]):
    url_factory: Callable[[int], str]
    total_pages: Collector[X, int]
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: Any) -> AsyncIterable[str]:
        total_pages = await self.total_pages(context, item)
        pages = map(self.url_factory, range(1, total_pages + 1))
        return AsyncIterableAdapter(pages)


