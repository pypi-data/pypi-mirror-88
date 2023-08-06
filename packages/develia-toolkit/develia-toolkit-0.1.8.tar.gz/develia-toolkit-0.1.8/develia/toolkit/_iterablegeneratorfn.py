import typing


@typing.final
class IterableGeneratorFn:
    def __init__(self, fn: typing.Callable, *args, **kwargs):
        self._function = fn
        self._args = args[:]
        self._kwargs = kwargs.copy()

    def __call__(self, *args, **kwargs):
        return self._function(*self._args, *self._kwargs)

    def __iter__(self):
        return self._function(*self._args, *self._kwargs)
