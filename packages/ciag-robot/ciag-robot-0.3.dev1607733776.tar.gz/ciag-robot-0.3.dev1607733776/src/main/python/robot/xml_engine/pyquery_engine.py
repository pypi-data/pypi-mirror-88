from __future__ import annotations
from typing import Iterator, Iterable, Callable, List
from robot.api import XmlEngine, XmlNode, O
from pyquery import PyQuery

import logging

logger = logging.getLogger(__name__)



class PyQueryNodeAdapter(XmlNode):

    logger = logger
    engine: PyQueryAdapter
    content: PyQuery
    
    def __init__(self, engine: PyQueryAdapter, content: PyQuery):
        self.engine = engine
        self.content = content


    def __iter__(self) -> Iterator[PyQueryNodeAdapter]:
        return self._map(self.content)

    def _map(self, pyquery: PyQuery) -> Iterator[PyQueryNodeAdapter]:
        for item in pyquery:
            yield PyQueryNodeAdapter(self.engine, self.engine.pyquery(item))

    
    def find_by_css(self, css: str) -> XmlNode:
        return PyQueryNodeAdapter(self.engine, self.content.find(css))

    def find_by_xpath(self, xpath: str) -> XmlNode:
        return PyQueryNodeAdapter(self.engine, self.engine.pyquery(self.content.root.xpath(xpath)))

    def cast(self, cast_fn: Callable[[XmlNode], O]) -> O:
        return cast_fn(next(iter(self)))

    def cast_all(self, cast_fn: Callable[[XmlNode], O]) -> List[O]:
        return list(map(cast_fn, self))

    def as_text(self) -> str:
        return self.content.text()

    def text(self) -> Iterable[str]:
        for item in self:
            yield item.content.text()

    def attr(self, attr: str) -> Iterable[str]:
        for item in self:
            yield item.content.attr(attr)

    def __repr__(self):
        return f'{self.__class__.__name__}{{ {self.content} }}'

    def __str__(self):
        return f'{self.__class__.__name__}{{ {self.content} }}'


class PyQueryAdapter(XmlEngine):

    logger = logger
    pyquery : PyQuery

    def __init__(self, pyquery = PyQuery):
        self.pyquery = pyquery


    def  __call__(self, raw_xml: str) -> PyQueryNodeAdapter:
        return PyQueryNodeAdapter(self, self.pyquery(raw_xml))