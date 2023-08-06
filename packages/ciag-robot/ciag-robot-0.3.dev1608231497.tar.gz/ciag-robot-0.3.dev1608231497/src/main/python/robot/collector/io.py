import logging
import os
from dataclasses import field, dataclass
from logging import Logger
from urllib.parse import urlparse

from robot.api import Collector, Context

__logger__ = logging.getLogger(__name__)


class FileNameCollector(Collector[str, str]):
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: str) -> str:
        parsed_url = urlparse(item)
        path, filename = parsed_url.path.rsplit('/', 1)
        path = os.path.join('.', path[1:])
        os.makedirs(path, exist_ok=True)
        return os.path.join(path, filename)


FILE_NAME_COLLECTOR = FileNameCollector()


@dataclass()
class DownloadCollector(Collector[str, str]):
    filename: Collector[str, str] = field(default=FILE_NAME_COLLECTOR)
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: str) -> str:
        filename = await self.filename(context, item)
        await context.download(item, filename)
        return filename
