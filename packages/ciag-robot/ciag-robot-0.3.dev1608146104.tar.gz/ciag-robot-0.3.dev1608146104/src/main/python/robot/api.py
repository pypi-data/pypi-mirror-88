from __future__ import annotations

from typing import List, Callable, Iterable, Iterator, Tuple, AsyncContextManager, Dict, Any
from typing import TypeVar, Generic

X = TypeVar('X')
Y = TypeVar('Y')


class HttpEngine():

    def session(self) -> HttpSession:
        raise NotImplementedError()


class HttpSession():

    async def download(self, url: str, filename: str):
        raise NotImplementedError()

    async def get(self, url):
        raise NotImplementedError()

    async def __aenter__(self):
        raise NotImplementedError()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError()

    async def close(self):
        raise NotImplementedError()


class XmlNode(Iterable['XmlNode']):

    def __iter__(self) -> Iterator[XmlNode]:
        raise NotImplementedError()

    def find_by_css(self, css: str) -> XmlNode:
        raise NotImplementedError()

    def find_by_xpath(self, xpath: str) -> XmlNode:
        raise NotImplementedError()

    def cast(self, cast_fn: Callable[[XmlNode], Y]) -> Y:
        raise NotImplementedError()

    def cast_all(self, cast_fn: Callable[[XmlNode], Y]) -> Iterable[Y]:
        raise NotImplementedError()

    def as_text(self) -> Iterable[str]:
        raise NotImplementedError()

    def attr(self, attr) -> Iterable[str]:
        raise NotImplementedError()


class XmlEngine():

    def __call__(self, raw_xml: str) -> XmlNode:
        raise NotImplementedError()


class Context():
    xml_engine: XmlEngine
    http_engine: HttpEngine

    async def close(self):
        raise NotImplementedError()

    def resolve_url(self, url: str) -> str:
        raise NotImplementedError()

    async def download(self, url: str, filename: str):
        raise NotImplementedError()

    async def http_get(self, url) -> Tuple[Context, XmlNode]:
        raise NotImplementedError()

    def __iter__(self):
        raise NotImplementedError()


class Collector(Generic[X, Y]):

    async def __call__(self, context: Context, item: X) -> Y:
        raise NotImplementedError()


class Robot():

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    async def run(self, collector: Collector[XmlNode, Y], url: str) -> Y:
        raise NotImplementedError()

    async def run_many(self, collector: Collector[XmlNode, Y], *urls: str) -> List[Y]:
        raise NotImplementedError()

    def sync_run(self, collector: Collector[XmlNode, Y], url: str) -> Y:
        raise NotImplementedError()

    def sync_run_many(self, collector: Collector[XmlNode, Y], *url: str) -> List[Y]:
        raise NotImplementedError()
