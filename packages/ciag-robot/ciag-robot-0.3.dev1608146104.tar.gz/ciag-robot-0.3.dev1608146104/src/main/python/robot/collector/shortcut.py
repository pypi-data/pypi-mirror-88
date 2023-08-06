from typing import Any, Dict

from robot.api import Collector, X
from robot.collector import core
# noinspection PyUnresolvedReferences
from robot.collector.core import AnyCollector as any
# noinspection PyUnresolvedReferences
from robot.collector.core import ArrayCollector as array
# noinspection PyUnresolvedReferences
from robot.collector.core import AsTextCollector as as_text
# noinspection PyUnresolvedReferences
from robot.collector.core import AsyncFnCollector as afn
# noinspection PyUnresolvedReferences
from robot.collector.core import AsyncTapCollector as atap
# noinspection PyUnresolvedReferences
from robot.collector.core import AttrCollector as attr
# noinspection PyUnresolvedReferences
from robot.collector.core import ChainCollector as chain
# noinspection PyUnresolvedReferences
from robot.collector.core import ConstCollector as const
# noinspection PyUnresolvedReferences
from robot.collector.core import CssCollector as css
# noinspection PyUnresolvedReferences
from robot.collector.core import CsvCollector as csv
# noinspection PyUnresolvedReferences
from robot.collector.core import DictCsvCollector as dict_csv
# noinspection PyUnresolvedReferences
from robot.collector.core import DefaultCollector as default
# noinspection PyUnresolvedReferences
from robot.collector.core import DelayCollector as delay
# noinspection PyUnresolvedReferences
from robot.collector.core import DownloadCollector as download
# noinspection PyUnresolvedReferences
from robot.collector.core import FilterCollector as filter
# noinspection PyUnresolvedReferences
from robot.collector.core import FnCollector as fn
# noinspection PyUnresolvedReferences
from robot.collector.core import GetCollector as get
# noinspection PyUnresolvedReferences
from robot.collector.core import JsonPathCollector as jsonpath
# noinspection PyUnresolvedReferences
from robot.collector.core import PagesCollector as pages
# noinspection PyUnresolvedReferences
from robot.collector.core import PipeCollector as pipe
# noinspection PyUnresolvedReferences
from robot.collector.core import RegexCollector as regex
# noinspection PyUnresolvedReferences
from robot.collector.core import StoreCollector as store
# noinspection PyUnresolvedReferences
from robot.collector.core import TapCollector as tap
# noinspection PyUnresolvedReferences
from robot.collector.core import TextCollector as text
# noinspection PyUnresolvedReferences
from robot.collector.core import TupleCollector as tuple
# noinspection PyUnresolvedReferences
from robot.collector.core import UrlCollector as url
# noinspection PyUnresolvedReferences
from robot.collector.core import XPathCollector as xpath

noop = lambda: core.NOOP_COLLECTOR

context = lambda: core.CONTEXT


def dict(*args: Collector[X, Dict[str, Any]], **kwargs: Collector[X, Any]) -> Collector[X, Dict[str, Any]]:
    return core.DictCollector(
        args,
        kwargs
    )


def obj(*args: Collector[X, Dict[str, Any]], **kwargs: Collector[X, Any]) -> Collector[X, core.Object]:
    dict_collector = core.DictCollector(
        args,
        kwargs
    )
    return core.ObjectCollector(dict_collector)
