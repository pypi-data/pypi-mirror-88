from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from itertools import chain
from logging import Logger
from typing import Any, AsyncIterable

from robot.api import Collector, Context, XmlNode, X, Y
from robot.collector.core import FILE_NAME_COLLECTOR, PipeCollector, ConstCollector, UrlCollector

__logger__ = logging.getLogger(__name__)


@dataclass()
class GetCollector(Collector[X, Y]):
    url: Collector[X, str]
    collector: Collector[XmlNode, Y]

    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: X) -> Y:
        url = await self.url(context, item)
        sub_context, sub_item = await context.http_get(url)
        result = await self.collector(sub_context, sub_item)
        return result


@dataclass()
class DownloadCollector(Collector[str, str]):
    filename: Collector[str, str] = field(default=FILE_NAME_COLLECTOR)
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: str) -> str:
        filename = await self.filename(context, item)
        await context.download(item, filename)
        return filename


@dataclass()
class GetManyCollector(Collector[Any, Any]):
    urls: Collector[Any, AsyncIterable[str]]
    collector: Collector[Any, Any]
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: Any) -> Any:
        tasks = []
        urls = await self.urls(context, item)
        async for url in urls:
            collector = GetCollector(PipeCollector(ConstCollector(url), UrlCollector()), self.collector)
            coro = collector(context, item)
            task = asyncio.create_task(coro)
            tasks.append(task)
        values = await asyncio.gather(*tasks)
        return values
