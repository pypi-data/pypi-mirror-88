import typing


class CachedIterable:
    def __init__(self, iterator: typing.Iterator):
        self._iterator = iterator
        self._cache = []

    def __iter__(self):
        for item in self._cache:
            yield item

        for item in self._iterator:
            self._cache.append(item)
            yield item
