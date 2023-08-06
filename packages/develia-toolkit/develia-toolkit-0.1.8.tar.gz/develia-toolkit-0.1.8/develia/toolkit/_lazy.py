import threading
import typing


@typing.final
class Lazy:
    def __init__(self, factory_method: typing.Callable[[], typing.Any]):
        self._factory_method = factory_method
        self._value_created = False
        self._value = None
        self._lock = threading.RLock()

    @property
    def value_created(self):
        return self._value_created

    @property
    def value(self):
        with self._lock:
            if not self._value_created:
                self._value = self._factory_method()
                self._value_created = True

            return self._value

    def __repr__(self):
        with self._lock:
            if self._value_created:
                return repr(self._value)

            return "Value not created yet."
