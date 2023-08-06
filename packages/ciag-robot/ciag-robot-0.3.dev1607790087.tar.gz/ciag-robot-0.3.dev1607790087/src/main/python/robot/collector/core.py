from __future__ import annotations
import asyncio
import logging
from dataclasses import dataclass, field
from logging import Logger
from typing import List, Any, Callable, Iterable, Dict, Tuple, Awaitable

from robot.api import Collector, Context, XmlNode, X, Y

__logger__ = logging.getLogger(__name__)


@dataclass(init=False)
class PipeCollector(Collector[Any, Any]):
    collectors: Tuple[Collector[Any, Any]]
    logger: Logger = field(default=__logger__, compare=False)

    def __init__(self, *collectors: Collector[Any, Any], logger=__logger__):
        self.collectors = collectors
        self.logger = logger

    async def __call__(self, context: Context, item: Any) -> Any:
        for collector in self.collectors:
            item = await collector(context, item)
        return item


@dataclass(init=False)
class DefaultCollector(Collector[Any, Any]):
    collectors: Tuple[Collector[Any, Any]]
    logger: Logger = field(default=__logger__, compare=False)

    def __init__(self, *collectors: Collector[Any, Any], logger=__logger__):
        self.collectors = collectors
        self.logger = logger

    def is_empty(self, value):
        if value is None:
            return True
        if isinstance(value, (str,)):
            if value.strip() == '':
                return True
            return False
        if isinstance(value, Iterable):
            for item in value:
                if not self.is_empty(item):
                    return False
            return True
        return False

    async def __call__(self, context: Context, item: Any) -> Any:
        for collector in self.collectors:
            result = await collector(context, item)
            if not self.is_empty(result):
                return result
        return None


@dataclass()
class FnCollector(Collector[X, Y]):
    fn: Callable[[X], Y]
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: X) -> Y:
        return self.fn(item)


@dataclass()
class AsyncFnCollector(Collector[X, Y]):
    fn: Callable[[X], Awaitable[Y]]
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: X) -> Y:
        return await self.fn(item)


@dataclass()
class NoopCollector(Collector[X, X]):
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: X) -> X:
        return item


NOOP_COLLECTOR = NoopCollector()


@dataclass()
class ConstCollector(Collector[Any, Y]):
    value: Y
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: Any) -> Y:
        return self.value


@dataclass()
class ArrayCollector(Collector[X, List[Y]]):
    splitter: Collector[X, Iterable[Any]]
    item_collector: Collector[Any, Y] = NOOP_COLLECTOR
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: X) -> Iterable[Y]:
        sub_items = await self.splitter(context, item)
        collected_items = await asyncio.gather(*[
            self.item_collector(context, sub_item)
            for sub_item in sub_items
        ])
        return collected_items


@dataclass(init=False)
class TupleCollector(Collector[X, Tuple]):
    collectors: Tuple[Collector[X, Any]]
    logger: Logger = field(default=__logger__, compare=False)

    def __init__(self, *collectors: Collector[X, Any], logger=__logger__):
        self.collectors = collectors
        self.logger = logger

    async def __call__(self, context: Context, item: X) -> Tuple:
        collected_items = await asyncio.gather(*[
            collector(context, item)
            for collector in self.collectors
        ])
        return collected_items


@dataclass()
class DelayCollector(Collector[X, X]):
    delay: float
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: X) -> X:
        await asyncio.sleep(self.delay)
        return item


@dataclass()
class DictCollector(Collector[X, Dict[str, Any]]):
    nested_collectors: Tuple[Collector[X, Dict[str, Any]]] = ()
    field_collectors: Dict[str, Collector[X, Any]] = field(default_factory=dict)
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: X) -> Dict[str, Any]:
        obj = dict()
        for collector in self.nested_collectors:
            result = await collector(context, item)
            obj.update(result)
        for attr_name, collector in self.field_collectors.items():
            obj[attr_name] = await collector(context, item)
        return obj


class Object(object):

    @classmethod
    def from_dict(cls, data: Dict) -> Object:
        return cls(dict([
            (k, v if not isinstance(v, dict) else cls.from_dict(v))
            for k, v in data.items()
        ]))

    def __init__(self, attributes):
        self.__dict__.update(attributes)

    def __eq__(self, other):
        if other is None:
            return False
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__dict__})'


@dataclass()
class ObjectCollector(Collector[X, Y]):
    dict_collector: DictCollector[X]
    cast: Callable[[Dict[str, Any]], Y] = field(default=Object.from_dict)
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: X) -> Dict[str, Any]:
        value = await self.dict_collector(context, item)
        result = self.cast(value)
        return result


@dataclass()
class CssCollector(Collector[XmlNode, XmlNode]):
    css_selector: str
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: XmlNode) -> XmlNode:
        return item.find_by_css(self.css_selector)


@dataclass()
class XPathCollector(Collector[XmlNode, XmlNode]):
    xpath: str
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: XmlNode) -> XmlNode:
        return item.find_by_xpath(self.xpath)


@dataclass()
class AsTextCollector(Collector[XmlNode, str]):
    prefix: str = ''
    suffix: str = ''
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: XmlNode) -> str:
        return self.prefix + item.as_text() + self.suffix


@dataclass()
class TextCollector(Collector[XmlNode, Iterable[str]]):
    prefix: str = ''
    suffix: str = ''
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: XmlNode) -> Iterable[str]:
        return [
            self.prefix + value + self.suffix
            for value in item.text()
        ]


@dataclass()
class AttrCollector(Collector[XmlNode, Iterable[str]]):
    attr: str
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: XmlNode) -> Iterable[str]:
        return [
            value
            for value in item.attr(self.attr)
        ]


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


@dataclass()
class AnyCollector(Collector[Iterable[X], X]):
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: Iterable[X]) -> X:
        return next(iter(item))


@dataclass()
class GetCollector(Collector[X, Y]):
    url_collector: Collector[X, str]
    collector: Collector[XmlNode, Y]

    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: X) -> Y:
        url = await self.url_collector(context, item)
        sub_context, sub_item = await context.http_get(url)
        result = await self.collector(sub_context, sub_item)
        return result
