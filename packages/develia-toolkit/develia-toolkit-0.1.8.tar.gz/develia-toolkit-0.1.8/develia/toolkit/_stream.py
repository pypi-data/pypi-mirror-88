import typing

import itertools

from ._iterablegeneratorfn import IterableGeneratorFn
from ._cachediterable import CachedIterable

_Predicate = typing.Union[typing.Callable[[typing.Any], bool], dict]
_Mapper = typing.Union[typing.Callable[[typing.Any], typing.Any], typing.Sequence[str]]


class Stream:


    @staticmethod
    def from_generator_fn(fn, *args, **kwargs):
        return Stream(IterableGeneratorFn(fn, *args, **kwargs))

    def __init__(self, iterable: typing.Iterable):
        if isinstance(iterable, typing.Iterator):
            self._iterable = CachedIterable(iterable)
        else:
            self._iterable = iterable

    @staticmethod
    def _to_predicate(arg: _Predicate) -> typing.Callable:
        if callable(arg):
            return arg

        if isinstance(arg, dict):
            def predicate(x):
                for k, v in arg.items():
                    if getattr(x, k) != v:
                        return False

                return True

            return predicate

    def filter(self, predicate: _Predicate) -> "Stream":
        return Stream.from_generator_fn(filter, self._to_predicate(predicate), self._iterable)

    def eval(self):
        return Stream(list(self._iterable))

    def cached(self):
        return Stream(CachedIterable(iter(self._iterable)))

    def map(self, mapper: _Mapper) -> "Stream":
        if callable(mapper):
            return Stream.from_generator_fn(map, mapper, self._iterable)
        if isinstance(mapper, list):
            return Stream([{attr: getattr(item, attr) for attr in mapper} for item in self._iterable])
        raise Exception

    def select(self, mapper: _Mapper) -> "Stream":
        return self.map(mapper)

    def __iter__(self):
        return iter(self._iterable)

    def first(self, predicate: typing.Optional[_Predicate] = None, fallback=None):
        collection = self.filter(predicate) if predicate else self._iterable
        for item in collection:
            return item

        return fallback

    def union(self, iterable):
        return Stream.from_generator_fn(itertools.chain, self._iterable, iterable)

    def single(self, predicate: typing.Optional[_Predicate] = None, fallback=None):
        if predicate:
            filtered = self.filter(predicate)
        else:
            filtered = self._iterable

        iterator = iter(filtered)

        try:
            item = next(iterator)
        except StopIteration:
            return fallback

        try:
            next(iterator)
            raise Exception
        except StopIteration:
            return item

    def to_list(self):
        return list(self._iterable)

    def _map_ranges(self, size, mapping=None):
        tmp = self._iterable if isinstance(self._iterable, list) else self._iterable
        if mapping:
            for i in range(len(tmp) - size):
                segment = tmp[i:i + size]
                yield mapping(Stream(segment))
        else:
            for i in range(len(tmp) - size):
                segment = tmp[i:i + size]
                yield Stream(segment)

    def map_ranges(self, size, mapping: typing.Optional[typing.Callable[["Stream"], typing.Any]] = None):
        return Stream.from_generator_fn(self._map_ranges, size, mapping)

    def __getitem__(self, idx):
        if hasattr(self._iterable, "typing.typing.getitemtyping.typing."):
            return self._iterable[idx]

        for i, item in enumerate(self):
            if i == idx:
                return item

    def __len__(self):
        if hasattr(self._iterable, "typing.typing.lentyping.typing."):
            return len(self._iterable)

        length = 0
        for _ in self._iterable:
            length += 1
        return length

    def __repr__(self):
        return list(self._iterable).__repr__()

    def index(self, item):
        for i, element in enumerate(self):
            if item == element:
                return i

    def min(self, selector=None):
        if selector is None:
            return min(self._iterable)
        else:
            return min(map(selector, self._iterable))

    def max(self, selector=None):
        if selector is None:
            return max(self._iterable)
        else:
            return max(map(selector, self._iterable))
