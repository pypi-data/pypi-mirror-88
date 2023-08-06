from typing import Any, Dict, Callable

from robot.api import Collector, X, Y
from robot.collector import core

const = core.ConstCollector
fn = core.FnCollector
noop = lambda: core.NOOP_COLLECTOR
afn = core.AsyncFnCollector
as_text = core.AsTextCollector
text = core.TextCollector
attr = core.AttrCollector
css = core.CssCollector
xpath = core.XPathCollector
pipe = core.PipeCollector
array = core.ArrayCollector
tuple = core.TupleCollector
any = core.AnyCollector
default = core.DefaultCollector
delay = core.DelayCollector
filter = core.FilterCollector
get = core.GetCollector
url = core.UrlCollector
regex = core.RegexCollector


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
