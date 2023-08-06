from __future__ import annotations
from robot.xml_engine.pyquery_engine import PyQueryAdapter
from robot.http_engine.aiohttp_engine import AioHttpAdapter
from robot.api import Context, XmlEngine, HttpEngine, HttpSession, XmlNode
from dataclasses import dataclass, field
from typing import Tuple, Any, Dict
from urllib.parse import urlparse


@dataclass()
class ContextImpl(Context):
    xml_engine: XmlEngine = field(default_factory=PyQueryAdapter)
    http_engine: HttpEngine = field(default_factory=AioHttpAdapter)
    url: Any = None
    http_headers: Dict[str, str] = field(default_factory=dict)
    http_session: HttpSession = None

    def clone(self, **override) -> ContextImpl:
        new_instance = self.__class__(**self.__dict__)
        for k, v in override.items():
            setattr(new_instance, k, v)
        return new_instance

    async def close(self):
        if self.http_session is None:
            return
        await self.http_session.close()
        self.http_session = None

    def get_http_session(self) -> HttpSession:
        if self.http_session is not None:
            return self.http_session
        self.http_session = self.http_engine.session()
        return self.http_session

    def resolve_url(self, url: str):
        if self.url is None:
            return url
        if '://' in url:
            return url
        if url.startswith('//'):
            return self.url.scheme + ':' + url
        if url.startswith('/'):
            return self.url.scheme + '://' + self.url.netloc + url
        base_path, _ = self.url.path.rsplit('/', 1)
        return ''.join([
            self.url.scheme,
            '://',
            self.url.netloc,
            base_path,
            '/',
            url,
        ])

    async def http_get(self, url) -> Tuple[Context, XmlNode]:
        session = self.get_http_session()
        url = self.resolve_url(url)
        headers, response = await session.get(url)
        return self.clone(
            url=urlparse(url),
            http_headers=headers,
            http_session=session,
        ), self.xml_engine(response)
