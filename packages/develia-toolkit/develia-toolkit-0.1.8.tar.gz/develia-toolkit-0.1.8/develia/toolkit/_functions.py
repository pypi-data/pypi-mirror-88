import math
from typing import Any as _Any, Type as _Type, Union as _Union, Callable, Any, Union


def iif(condition, if_true: Union[Any, Callable[[], Any]], otherwise=Union[Any, Callable[[], Any]]) -> Any:
    if condition:
        return if_true
    return otherwise


def value(obj):
    if callable(obj):
        return obj()
    return obj


def coalesce(*args) -> _Any:
    if args is None:
        return None

    for item in args:
        if item is not None:
            return item
    return None


def is_float(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False


def is_int(string: str) -> bool:
    try:
        int(string)
        return True
    except ValueError:
        return False


def parse(target_type: _Type[_Union[int, float]], string: str,
          decimal_separator: str = ".",
          thousands_separator: str = None,
          fallback: _Any = None) -> _Any:
    if thousands_separator is not None:
        string = string.replace(thousands_separator, "")

    try:
        if target_type == float:
            if decimal_separator != ".":
                string = string.replace(decimal_separator, ".")
            return float(string)
        elif target_type == int:
            return int(string)

        return fallback() if callable(fallback) else fallback
    except ValueError:
        return fallback() if callable(fallback) else fallback
