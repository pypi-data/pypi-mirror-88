import asyncio
from robot.api import Collector, Context, XmlNode, I, O
from typing import List, Any, Callable, Awaitable, Iterable, Dict
import logging


logger = logging.getLogger(__name__)

class PipeCollector(Collector[Any, Any]):

    logger = logger

    def __init__(self, *collectors : List[Collector[Any, Any]]):
        self.collectors = collectors

    async def __call__(self, context: Context, item: Any) -> Any:
        for collector in self.collectors:
            item = await collector(context, item)
        return item


class DefaultCollector(Collector[Any, Any]):

    logger = logger

    def __init__(self, *collectors : List[Collector[Any, Any]]):
        self.collectors = collectors

    async def __call__(self, context: Context, item: Any) -> Any:
        for collector in self.collectors:
            item = await collector(context, item)
            if item: return item
        return item


class FnCollector(Collector[I,O]):

    logger = logger

    fn : Callable[[Context,I], O]

    def __init__(self, fn: Callable[[Context, I], O] ):
        self.fn = fn

    async def __call__(self, context: Context, item: I) -> O:
        return self.fn(context, item)


class AsyncCollector(Collector[I,O]):

    logger = logger

    fn : Callable[[Context,I], O]

    def __init__(self, fn: Callable[[Context, I], Awaitable[O]]):
        self.fn = fn

    async def __call__(self, context: Context, item: I) -> O:
        return await self.fn(context, item)



class NoopCollector(Collector[I,I]):

    logger = logger

    async def __call__(self, context: Context, item: I) -> I:
        return item

NOOP_COLLECTOR = NoopCollector()


class ArrayCollector(Collector[I, List[O]]):

    logger = logger

    def __init__(self, splitter: Collector[I, List[Any]], collector : Collector[Any, O] = NOOP_COLLECTOR):
        self.splitter = splitter
        self.collector = collector

    async def __call__(self, context: Context, item : I) -> Iterable[O]:
        sub_items = await self.splitter(context, item)
        collected_items = await asyncio.gather(*[self.collector(context, sub_item) for sub_item in sub_items])
        return collected_items


class DictCollector(Collector[I, Dict[str,Any]]) :

    logger = logger

    def __init__(self,nested_collectors: List[Collector[I, Dict[str, Any]]], collectors_map : Dict[str, Collector[I, Any]]):
        self.nested_collectors = nested_collectors
        self.collectors_map = collectors_map

    async def __call__(self, context: Context, item: I) -> Dict[str, Any]:
        pass
        

class CssCollector(Collector[XmlNode, XmlNode]):

    logger = logger

    def __init__(self, css_selector: str):
        self.css_selector = css_selector

    async def __call__(self, context: Context, item: XmlNode) -> XmlNode:
        return item.find_by_css(self.css_selector)


class AsTextCollector(Collector[XmlNode, str]):

    logger = logger

    def __init__(self, prefix='', suffix=''):
        self.prefix = prefix
        self.suffix = suffix

    async def __call__(self, context: Context, item: XmlNode) -> str:
        return self.prefix + item.as_text() + self.suffix

class TextCollector(Collector[XmlNode, Iterable[str]]):

    logger = logger

    def __init__(self, prefix='', suffix=''):
        self.prefix = prefix
        self.suffix = suffix

    async def __call__(self, context: Context, item: XmlNode) -> Iterable[str]:
        return [
            self.prefix + value + self.suffix
            for value in item.text()
        ]


class AttrCollector(Collector[XmlNode, Iterable[str]]):

    logger = logger

    def __init__(self, attr: str, prefix='', suffix=''):
        self.prefix = prefix
        self.suffix = suffix
        self.attr = attr

    async def __call__(self, context: Context, item: XmlNode) -> Iterable[str]:
        return [
            self.prefix + value + self.suffix
            for value in  item.attr(self.attr)
        ]


class AnyCollector(Collector[Iterable[I],I]):

    logger = logger

    async def __call__(self, context: Context, item: Iterable[I]) -> I:
        return next(iter(item))