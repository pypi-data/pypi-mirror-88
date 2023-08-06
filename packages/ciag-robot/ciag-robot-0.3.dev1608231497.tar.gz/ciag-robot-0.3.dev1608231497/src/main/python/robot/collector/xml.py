import logging
from dataclasses import dataclass, field
from logging import Logger
from typing import Iterable

from robot.api import Collector, XmlNode, Context

__logger__ = logging.getLogger(__name__)


@dataclass()
class XPathCollector(Collector[XmlNode, XmlNode]):
    xpath: str
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: XmlNode) -> XmlNode:
        return item.find_by_xpath(self.xpath)


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