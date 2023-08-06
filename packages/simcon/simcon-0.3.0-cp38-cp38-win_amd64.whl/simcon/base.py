import asyncio
import dataclasses
import threading
import typing

from collections import deque
from . import _native


T = typing.TypeVar("T")


@dataclasses.dataclass  # For smoother inheritance
class AsyncNotifierThreadSafe:
    _waiters: "deque[asyncio.Future]" = dataclasses.field(default_factory=deque, init=False)
    _lock: threading.Lock = dataclasses.field(default_factory=threading.RLock, init=False)  # Use in child classes for synchronisation

    def add_waiter(self) -> asyncio.Future:
        waiter = asyncio.get_event_loop().create_future()
        self._waiters.append(waiter)
        return waiter

    def notify_all(self) -> None:
        for waiter in self._waiters:

            def notify():
                try:
                    waiter.set_result(None)
                except asyncio.InvalidStateError:  # Future cancelled
                    pass

            try:
                waiter.get_loop().call_soon_threadsafe(notify)
            except RuntimeError:  # Loop isn't running
                continue

        self._waiters.clear()

    def notify_one(self) -> None:
        while True:  # Try all waiters until one succeeds or none are left
            try:
                waiter = self._waiters.popleft()
            except IndexError:  # Empty list
                return

            def notify_fallback():
                try:
                    waiter.set_result(None)
                except asyncio.InvalidStateError:  # Future cancelled
                    self.notify_one()

            try:
                waiter.get_loop().call_soon_threadsafe(notify_fallback)
                return
            except RuntimeError:  # Loop isn't running
                continue


class SimException(Exception):

    msg_exc: _native.MsgException

    def __init__(self, msg_exc: _native.MsgException) -> None:
        message = _native.EXCEPTION(msg_exc.dwException).name
        super().__init__(message)
        self.msg_exc = msg_exc


@dataclasses.dataclass
class HasExceptions(AsyncNotifierThreadSafe):
    packet_ids: typing.List[int]

    _exception: typing.Optional[Exception] = dataclasses.field(default=None, init=False)

    def set_exception(self, msg_exc: _native.MsgException):
        assert msg_exc.dwSendID in self.packet_ids
        with self._lock:
            self._exception = SimException(msg_exc)
            self.notify_all()

    def set_python_exception(self, exc: Exception):
        with self._lock:
            self._exception = exc
            self.notify_all()

    def check_exception(self):
        if self._exception:
            raise self._exception


class Closed(Exception):
    pass


@dataclasses.dataclass
class Closeable(AsyncNotifierThreadSafe):

    _closed: bool = dataclasses.field(default=False, init=False)

    def close(self):
        with self._lock:
            self._closed = True
            self.notify_all()

    def check_closed(self):
        if self._closed:
            raise Closed
