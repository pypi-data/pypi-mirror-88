from threading import Thread as _Thread
from functools import wraps as _wraps
from typing import List as _List, Callable as _Callable, Optional as _Optional


def threaded(daemon: _Optional[bool] = None, **kwargs):
    def inner(func):
        @_wraps(func)
        def innermost(*inner_args, **inner_kwargs) -> _Thread:
            result = [None]

            def run():
                # noinspection PyBroadException
                try:
                    result[0] = func(*inner_args, **inner_kwargs)
                except Exception as ex:
                    raise ex

            thread1 = _Thread(target=run, daemon=daemon, **kwargs)
            thread1.start()

            return thread1
            # def awaiter():
            #     thread1.join()
            #     return result[0]
            #
            # return awaiter

        return innermost

    return inner
