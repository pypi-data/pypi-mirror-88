import asyncio
import threading
import typing
import weakref

from .utils import GlobalEvent, AutoincrementDWORD, no_async
from .base import HasExceptions
from .data import DataField, DataRequest
from .events import SystemEvent, SystemEventType
from . import _native
from ._native import PERIOD


class Sim:

    OPEN_TIMEOUT_SEC: float = 5

    _sim: _native.Sim
    _loop_thr: typing.Optional[threading.Thread] = None
    _stopping: bool = False
    _lock: threading.Lock  # Instance-wide consistency lock
    _open_evt: GlobalEvent
    _loop_done_evt = GlobalEvent
    _event_id_inc: AutoincrementDWORD
    _data_request_id_inc: AutoincrementDWORD
    _definition_id_inc: AutoincrementDWORD
    _events: typing.Dict[int, "weakref.ref[SystemEvent]"]  # weakref.ref is not Generic in runtime
    _data_requests: typing.Dict[int, "weakref.ref[DataRequest]"]
    _data_definition_ids: typing.Set[int]
    _exception_targets: typing.Dict[int, "weakref.ref[HasExceptions]"]
    open_msg: typing.Optional[_native.MsgOpen] = None

    def __init__(self, app_name: str) -> None:
        self._open_evt = GlobalEvent(packet_ids=[1])
        self._loop_done_evt = GlobalEvent(packet_ids=[-1])
        self._lock = threading.Lock()

        self._event_id_inc = AutoincrementDWORD()
        self._data_request_id_inc = AutoincrementDWORD()
        self._definition_id_inc = AutoincrementDWORD()
        self._events = {}
        self._data_requests = {}
        self._data_definition_ids = set()
        self._exception_targets = {
            self._open_evt.packet_ids[0]: weakref.ref(self._open_evt)
        }

        self._sim = _native.Sim(app_name)

    async def __aenter__(self) -> "Sim":
        self._loop_thr = threading.Thread(target=self._loop, daemon=True)
        self._loop_thr.start()
        await self.wait_open(self.OPEN_TIMEOUT_SEC)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        self._stopping = True
        self._sim.interrupt_receive()
        await self._loop_done_evt.wait()
        self._loop_thr = None

    async def wait_open(self, timeout: typing.Optional[float] = None) -> None:
        await self._open_evt.wait(timeout)

    def subscribe_to_system_event(self, event_type: events.SystemEventType) -> SystemEvent:
        # TODO: Add explicit unsubscribe
        # No locking here. Hoping that the counter will not wrap around and reach our value again
        # before the code below completes.
        event_id = self._event_id_inc.next(self._events)

        def clean_event(_):
            self._sim.unsubscribe_from_system_event(event_id)
            self._events.pop(event_id)
            self._exception_targets.pop(packet_id)
            print(f"Cleaned event #{event_id}")

        with self._lock:
            self._sim.subscribe_to_system_event(event_id, event_type)
            packet_id = self._sim.get_last_sent_packet_id()
            event = SystemEvent(packet_ids=[packet_id], event_id=event_id)
            ref = weakref.ref(event, clean_event)
            self._events[event_id] = ref
            self._exception_targets[packet_id] = ref

        return event

    def request_data_on_sim_object(self, fields: typing.List[DataField], period: PERIOD, object_id: int = 0):
        # TODO: Add explicit unsubscribe
        definition_id = self._definition_id_inc.next(self._data_definition_ids)
        request_id = self._data_request_id_inc.next(self._data_requests)
        packet_ids = []

        def clean_data_request(_):
            # TODO: unsubscribe from data!
            self._data_definition_ids.discard(definition_id)
            self._data_requests.pop(request_id)
            for packet_id in packet_ids:
                self._exception_targets.pop(packet_id)
            print(f"Cleaned data request #{request_id}")

        with self._lock:
            for field in fields:
                self._sim.add_to_data_definition(definition_id, field.name, field.units)
                packet_ids.append(self._sim.get_last_sent_packet_id())
            self._sim.request_data_on_sim_object(request_id, definition_id, object_id, period)
            data_request = DataRequest(
                packet_ids=packet_ids,
                fields=fields,
            )
            ref = weakref.ref(data_request, clean_data_request)
            self._data_requests[request_id] = ref
            for packet_id in packet_ids:
                self._exception_targets[packet_id] = ref

        return data_request

    def _process_event(self, msg: _native.MsgEvent):
        with self._lock:
            event = self._events.get(msg.uEventID)
        if event is None:
            return
        event = event()  # dereference the weakref
        if event is None:
            return
        event.send_event(msg)

    def _process_exception(self, msg: _native.MsgException):
        with self._lock:
            target = self._exception_targets.get(msg.dwSendID)
        if target is None:
            return
        target = target()  # dereference the weakref
        if target is None:
            return
        target.set_exception(msg)

    def _process_data(self, msg: _native.MsgSimobjectData):
        with self._lock:
            data_request = self._data_requests.get(msg.dwRequestID)
        if data_request is None:
            return
        data_request = data_request()  # dereference the weakref
        if data_request is None:
            return
        data_request.send_data(msg)

    def _loop(self) -> None:
        while not self._stopping:
            msg = self._sim.receive()
            base = msg.as_base()
            if base is None:
                continue
            msg_type = _native.RECV_ID(base.dwID)
            if msg_type == _native.RECV_ID.OPEN:
                self.open_msg = msg.as_open()
                self._open_evt.set()
            elif msg_type == _native.RECV_ID.EVENT:
                self._process_event(msg.as_event())
            elif msg_type == _native.RECV_ID.EVENT_FRAME:
                self._process_event(msg.as_event())
            elif msg_type == _native.RECV_ID.SIMOBJECT_DATA:
                self._process_data(msg.as_simobject_data())
            elif msg_type == _native.RECV_ID.EXCEPTION:
                self._process_exception(msg.as_exception())

            # print(_native.RECV_ID(base.dwID))

        self._loop_done_evt.set()

    ########################
    # Synchronous interface
    ########################

    @no_async
    def __enter__(self) -> "Sim":
        return asyncio.run(self.__aenter__())

    @no_async
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        return asyncio.run(self.__aexit__(exc_type, exc_val, exc_tb))

    @no_async
    def sync_wait_open(self) -> None:
        return asyncio.run(self.wait_open())
