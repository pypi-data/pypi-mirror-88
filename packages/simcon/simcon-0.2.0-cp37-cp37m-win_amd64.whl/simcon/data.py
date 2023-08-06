import asyncio
import dataclasses
import struct
import typing

from . import _native
from .base import HasExceptions, Closeable
from .utils import no_async


@dataclasses.dataclass
class DataField:
    name: str
    units: str
    struct_format: str = "d"


DataType = typing.Optional[typing.Dict[str, typing.Any]]


@dataclasses.dataclass
class DataRequest(HasExceptions, Closeable):

    fields: typing.List[DataField]

    _data: DataType = dataclasses.field(default=None, init=False, repr=False)

    def send_data(self, simobject_data: _native.MsgSimobjectData) -> None:
        with self._lock:
            if self._data is not None:
                print("Warning: data point was lost")  # FIXME: Use logging may be?
            self._data = self.parse_data(simobject_data)
            self.notify_one()

    def parse_data(self, simobject_data: _native.MsgSimobjectData) -> DataType:
        struct_format = "".join(df.struct_format for df in self.fields)
        keys = [df.name for df in self.fields]
        values = struct.unpack(struct_format, simobject_data.data)
        assert len(keys) == len(values)
        return dict(zip(keys, values))

    async def wait(self) -> DataType:
        while True:
            with self._lock:
                self.check_exception()
                self.check_closed()
                if self._data is not None:
                    data = self._data
                    self._data = None
                    return data
                waiter = self.add_waiter()
            await waiter
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
    def sync_wait(self) -> _native.MsgEvent:
        return asyncio.run(self.wait())

    @no_async
    def __next__(self):
        return asyncio.run(self.__anext__())

    @no_async
    def __iter__(self):
        return self
