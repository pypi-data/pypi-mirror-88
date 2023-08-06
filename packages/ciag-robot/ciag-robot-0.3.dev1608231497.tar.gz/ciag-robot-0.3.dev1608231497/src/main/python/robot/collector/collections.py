import logging
from dataclasses import dataclass, field
from itertools import chain
from logging import Logger
from typing import Iterable, List, Callable

from robot.api import Collector, X, Context

__logger__ = logging.getLogger(__name__)


@dataclass()
class FlatCollector(Collector[Iterable[Iterable[X]], List[X]]):
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: Iterable[Iterable[X]]) -> List[X]:
        return list(chain(*item))


FLAT_COLLECTOR = FlatCollector()


@dataclass()
class ChainCollector(Collector[Iterable[Iterable[X]], Iterable[X]]):
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: Iterable[Iterable[X]]) -> Iterable[X]:
        return chain(*item)


CHAIN_COLLECTOR = ChainCollector()


@dataclass()
class AnyCollector(Collector[Iterable[X], X]):
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: Iterable[X]) -> X:
        return next(iter(item))


@dataclass()
class FilterCollector(Collector):
    predicate: Callable[[X], bool]
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: Iterable) -> Iterable:
        return [
            value
            for value in item
            if self.predicate(value)
        ]
