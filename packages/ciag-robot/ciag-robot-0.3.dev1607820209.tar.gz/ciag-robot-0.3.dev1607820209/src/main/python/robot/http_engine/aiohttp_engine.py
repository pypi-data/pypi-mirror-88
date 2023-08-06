import asyncio
from typing import TypeVar, Tuple, Any

import aiohttp

from robot.api import HttpSession, HttpEngine

T = TypeVar('T')


class AioHttpSessionAdapter(HttpSession):
    client_session: aiohttp.ClientSession

    def __init__(self, client_session: aiohttp.ClientSession):
        self.client_session = client_session

    async def get(self, url) -> Tuple[Any, str]:
        async with self.client_session.get(url, allow_redirects=True) as response:
            content = await response.content.read()
            return response.headers, content

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self.close()

    async def close(self):
        return await self.client_session.close()


class AioHttpAdapter(HttpEngine):
    def __init__(self, aiohttp=aiohttp):
        self.aiohttp = aiohttp

    def session(self) -> HttpSession:
        return AioHttpSessionAdapter(self.aiohttp.ClientSession())
