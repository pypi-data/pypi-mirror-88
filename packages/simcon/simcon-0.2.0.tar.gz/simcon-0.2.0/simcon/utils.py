import asyncio
import dataclasses
import functools
import threading
import typing

from .base import HasExceptions, Closeable


@dataclasses.dataclass()
class GlobalEvent(HasExceptions, Closeable):

    _value: bool = dataclasses.field(default=False, init=False)
    _lock: threading.Lock = dataclasses.field(default_factory=threading.Lock, init=False)

    def is_set(self) -> bool:
        return self._value

    async def wait(self, timeout: typing.Optional[float] = None) -> None:
        with self._lock:
            self.check_exception()
            self.check_closed()
            if self._value:
                return
            waiter = self.add_waiter()
        await asyncio.wait_for(waiter, timeout)
        self.check_exception()
        self.check_closed()

    def set(self) -> None:
        with self._lock:
            if self._value:
                return
            self._value = True
            self.notify_all()

    def clear(self) -> None:
        self._value = False


class Autoincrement:

    _last_value: typing.Optional[int]
    _max_value = typing.Optional[int]
    _lock: threading.Lock

    def __init__(self, last_value: int = None, max_value: int = None):
        self._last_value = last_value
        self._max_value = None
        self._lock = threading.Lock()

    @property
    def last_value(self) -> int:
        return self._last_value

    def next(self, skip: typing.Optional[typing.Iterable] = None) -> int:
        with self._lock:
            while True:
                if self._last_value is None:
                    self._last_value = 0
                else:
                    self._last_value += 1
                if self._max_value is not None and self._last_value > self._max_value:
                    self._last_value = 0
                if skip is None or self._last_value not in skip:
                    return self._last_value


class AutoincrementDWORD(Autoincrement):

    def __init__(self, last_value: int = None):
        super().__init__(last_value=last_value, max_value=2**32 - 1)


def no_async(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            asyncio.get_running_loop()
            raise Exception("This code cannot run in asyncio loops. Use async interface instead")
        except RuntimeError:  # No running loop, as expected
            pass
        return func(*args, **kwargs)
    return wrapper
