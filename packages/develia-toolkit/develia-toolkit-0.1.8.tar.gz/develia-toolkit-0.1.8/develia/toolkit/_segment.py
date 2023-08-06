from functools import wraps
from typing import Sequence, Union, final


@final
class Segment:

    @property
    def stop(self):
        return self._stop

    @property
    def start(self):
        return self._stop

    def __init__(self, sequence: Union[Sequence, 'Segment'], start: int, stop: int = None, count: int = None):

        assert not (stop is not None and count is not None)

        if count is not None:
            self._stop = start + count
            assert self._stop <= len(sequence)
        elif stop is not None:
            self._stop = stop
        else:
            self._stop = len(sequence)

        self._start = start
        self._sequence: Union[Sequence, 'Segment'] = sequence

    def __getitem__(self, item):
        if isinstance(item, slice):
            start = item.start + self._start
            stop = start + item.stop
            return self._sequence[start:stop: item.step]

        return self._sequence[item]

    def __setitem__(self, item: int, value):
        if isinstance(item, slice):
            start = item.start + self._start
            stop = start + item.stop
            self._sequence[start:stop: item.step] = value

        self._sequence[item + self._start] = value

    def __iter__(self):
        for x in range(self._start, self._stop):
            yield self._sequence[x]

    def __len__(self):
        return self._stop - self._start

    def __repr__(self):
        return self._sequence[self._start:self._stop].__repr__()
