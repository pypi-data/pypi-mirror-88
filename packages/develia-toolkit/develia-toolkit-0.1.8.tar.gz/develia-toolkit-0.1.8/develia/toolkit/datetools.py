from datetime import datetime as _datetime, time as _time, date as _date
from datetime import timedelta as _timedelta
import typing as _typing


def start_of_day(input_date: _date) -> _datetime:
    return _datetime.combine(input_date, _time())


def end_of_day(input_date: _date) -> _datetime:
    return _datetime.combine(input_date, _time(23, 59, 59, 59))


def get_unix_timestamp(date: _typing.Union[_date, _datetime]) -> float:
    return (date - _datetime(1970, 1, 1)).total_seconds()


def datetime_from_unix_timestamp(unix_timestamp: float) -> _datetime:
    return _datetime(1970, 1, 1) + _timedelta(seconds=unix_timestamp)


def truncate(datetime: _datetime, timedelta: _timedelta):
    unix_timestamp = get_unix_timestamp(datetime)
    timedelta_total_seconds = timedelta.total_seconds()
    surplus = unix_timestamp % timedelta_total_seconds
    return datetime_from_unix_timestamp(unix_timestamp - surplus)
