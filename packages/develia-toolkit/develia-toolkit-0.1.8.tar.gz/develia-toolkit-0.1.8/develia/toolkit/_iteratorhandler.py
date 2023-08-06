import typing

T = typing.TypeVar("T")


@typing.final
class IteratorHandler:
    def __init__(self, iterator: typing.Iterator[T]):
        self._iterator = iter(iterator)
        self._current = None

    def __next__(self):
        return next(self._iterator)

    def __iter__(self):
        return self

    def next(self) -> bool:
        try:
            self._current = next(self._iterator)
            return True
        except StopIteration:
            return False

    @property
    def current(self) -> T:
        return self._current
