import logging
import re
from dataclasses import dataclass, field
from logging import Logger
from typing import Union, Sequence

from robot.api import Collector, Context

__logger__ = logging.getLogger(__name__)


@dataclass(init=False)
class RegexCollector(Collector[str, str]):
    logger: Logger = field(default=__logger__, compare=False)

    def __init__(self, regex, logger=__logger__):
        if isinstance(regex, (str,)):
            regex = re.compile(regex)
        self.regex = regex
        self.logger = logger

    async def __call__(self, context: Context, item: str) -> Union[str, Sequence[str]]:
        match = self.regex.search(item)
        if not match:
            return None
        group_dict = match.groupdict()
        if group_dict:
            return group_dict
        groups = match.groups()
        if len(groups) > 1:
            return groups
        elif groups:
            return groups[0]
        return match.group(0)
