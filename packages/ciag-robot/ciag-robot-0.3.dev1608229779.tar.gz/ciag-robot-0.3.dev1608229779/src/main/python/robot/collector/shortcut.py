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
from robot.collector.core import AttrCollector as attr
# noinspection PyUnresolvedReferences
from robot.collector.core import ConstCollector as const
# noinspection PyUnresolvedReferences
from robot.collector.core import DefaultCollector as default
# noinspection PyUnresolvedReferences
from robot.collector.core import DelayCollector as delay
# noinspection PyUnresolvedReferences
from robot.collector.core import FilterCollector as filter
# noinspection PyUnresolvedReferences
from robot.collector.core import FnCollector as fn
# noinspection PyUnresolvedReferences
from robot.collector.core import PipeCollector as pipe
# noinspection PyUnresolvedReferences
from robot.collector.core import RegexCollector as regex
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
# noinspection PyUnresolvedReferences
from robot.collector.css import CssCollector as css
# noinspection PyUnresolvedReferences
from robot.collector.http import GetCollector as get, DownloadCollector as download, GetManyCollector as get_many
# noinspection PyUnresolvedReferences
from robot.collector.json import JsonPathCollector as jsonpath
# noinspection PyUnresolvedReferences
# noinspection PyUnresolvedReferences
from robot.collector.pagination import PagesUrlCollector as pages
# noinspection PyUnresolvedReferences
from robot.collector.store import StoreCollector as store, CsvCollector as csv, DictCsvCollector as dict_csv

noop = lambda: core.NOOP_COLLECTOR

context = lambda: core.CONTEXT

flat = lambda: core.FLAT_COLLECTOR

chain = lambda: core.CHAIN_COLLECTOR


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
