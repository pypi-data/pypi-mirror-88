import asyncio
import dataclasses
import enum

from collections import deque
from . import _native
from .utils import no_async
from .base import HasExceptions, Closeable


class SystemEventType(str, enum.Enum):
    Sec_1 = "1sec"
    Sec_4 = "4sec"
    Hz_6 = "6Hz"
    AircraftLoaded = "AircraftLoaded"
    Crashed = "Crashed"
    CrashReset = "CrashReset"
    FlightLoaded = "FlightLoaded"
    FlightSaved = "FlightSaved"
    FlightPlanActivated = "FlightPlanActivated"
    FlightPlanDeactivated = "FlightPlanDeactivated"
    Frame = "Frame"
    Pause = "Pause"
    Paused = "Paused"
    PauseFrame = "PauseFrame"
    PositionChanged = "PositionChanged"
    Sim = "Sim"
    SimStart = "SimStart"
    SimStop = "SimStop"
    Sound = "Sound"
    Unpaused = "Unpaused"
    View = "View"
    WeatherModeChanged = "WeatherModeChanged"
    AI = "AI"
    ObjectAdded = "ObjectAdded"
    ObjectRemoved = "ObjectRemoved"



@dataclasses.dataclass
class SystemEvent(HasExceptions, Closeable):
    event_id: int

    _events: "deque[_native.MsgEvent]" = dataclasses.field(default_factory=deque, init=False)

    def send_event(self, msg_event: _native.MsgEvent) -> None:
        with self._lock:
            self._events.append(msg_event)
            self.notify_one()

    async def wait(self) -> _native.MsgEvent:
        while True:
            with self._lock:
                self.check_exception()
                self.check_closed()
                try:
                    return self._events.pop()
                except IndexError:  # no pending events
                    pass
                waiter = self.add_waiter()
            await waiter
            self.check_exception()
            self.check_closed()
            try:
                return self._events.pop()
            except IndexError:  # Someone was faster
                continue

    async def __anext__(self) -> _native.MsgEvent:
        return await self.wait()

    def __aiter__(self):
        return self

    ########################
    # Synchronous interface
    ########################

    def sync_wait(self) -> _native.MsgEvent:
        return asyncio.run(self.wait())

    @no_async
    def __next__(self):
        return asyncio.run(self.__anext__())

    @no_async
    def __iter__(self):
        return self
