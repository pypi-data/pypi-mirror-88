import asyncio
import dataclasses
import struct
import typing

from simcon import _native
from simcon.base import HasExceptions, Closeable
from simcon.utils import no_async
from . import types


@dataclasses.dataclass
class DataField:
    name: str
    units: typing.Optional[str]
    type: types.Type = types.FLOAT64

    def __post_init__(self):
        if not self.type.unitless and self.units is None:
            raise ValueError(f"{self.type} requires non-empty units")


DataType = typing.Optional[typing.Dict[str, typing.Any]]


@dataclasses.dataclass
class DataRequest(HasExceptions, Closeable):

    fields: typing.List[DataField]

    _data: DataType = dataclasses.field(default=None, init=False, repr=False)

    def send_data(self, simobject_data: _native.MsgSimobjectData) -> None:
        with self._lock:
            if self._data is not None:
                print("Warning: data point was lost")  # FIXME: Use logging may be?
            try:
                self._data = self.parse_data(simobject_data)
            except Exception as exc:
                self.set_python_exception(exc)
                return
            self.notify_one()

    def parse_data(self, simobject_data: _native.MsgSimobjectData) -> DataType:
        formats = []
        for data_field in self.fields:
            formats.append(data_field.type.struct_fmt)

        struct_format = "".join(formats)
        struct_size = struct.calcsize(struct_format)
        values = struct.unpack(struct_format, simobject_data.get_bytes(struct_size))
        assert len(self.fields) == len(values)
        result = {}
        for pos, data_field in enumerate(self.fields):
            result[data_field.name] = data_field.type.convert(values[pos])
        return result

    async def wait(self, timeout: typing.Optional[float] = None) -> DataType:
        while True:
            with self._lock:
                self.check_exception()
                self.check_closed()
                if self._data is not None:
                    data = self._data
                    self._data = None
                    return data
                waiter = self.add_waiter()

            await asyncio.wait_for(waiter, timeout=timeout)
            self.check_exception()
            self.check_closed()
            with self._lock:
                if self._data is not None:
                    data = self._data
                    self._data = None
                    return data
                continue

    async def __anext__(self) -> typing.Optional[typing.Dict[str, typing.Any]]:
        return await self.wait()

    def __aiter__(self):
        return self

    ########################
    # Synchronous interface
    ########################

    @no_async
    def sync_wait(self, timeout: typing.Optional[float] = None) -> _native.MsgEvent:
        return asyncio.run(self.wait(timeout))

    @no_async
    def __next__(self):
        return asyncio.run(self.__anext__())

    @no_async
    def __iter__(self):
        return self
