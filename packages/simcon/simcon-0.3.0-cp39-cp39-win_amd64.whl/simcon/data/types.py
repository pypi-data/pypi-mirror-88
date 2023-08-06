import dataclasses
import typing

from simcon._native import DATATYPE


@dataclasses.dataclass
class Type:
    data_type: DATATYPE
    struct_fmt: str
    unitless: bool = False
    converter: typing.Optional[typing.Callable[[typing.Any], typing.Any]] = None

    def convert(self, val: typing.Any) -> typing.Any:
        if self.converter is None:
            return val
        return self.converter(val)


def string_converter(string):
    return string.rstrip(b"\000").decode()


INT32 = Type(
    data_type=DATATYPE.INT32,
    struct_fmt="i",
)


INT64 = Type(
    data_type=DATATYPE.INT64,
    struct_fmt="q",
)


FLOAT32 = Type(
    data_type=DATATYPE.FLOAT32,
    struct_fmt="f",
)


FLOAT64 = Type(
    data_type=DATATYPE.FLOAT64,
    struct_fmt="d",
)


STRING8 = Type(
    data_type=DATATYPE.STRING8,
    struct_fmt="8s",
    unitless=True,
    converter=string_converter,
)


STRING32 = Type(
    data_type=DATATYPE.STRING32,
    struct_fmt="32s",
    unitless=True,
    converter=string_converter,
)


STRING64 = Type(
    data_type=DATATYPE.STRING64,
    struct_fmt="64s",
    unitless=True,
    converter=string_converter,
)


STRING128 = Type(
    data_type=DATATYPE.STRING128,
    struct_fmt="128s",
    unitless=True,
    converter=string_converter,
)


STRING256 = Type(
    data_type=DATATYPE.STRING256,
    struct_fmt="256s",
    unitless=True,
    converter=string_converter,
)


STRING260 = Type(
    data_type=DATATYPE.STRING260,
    struct_fmt="260s",
    unitless=True,
    converter=string_converter,
)

