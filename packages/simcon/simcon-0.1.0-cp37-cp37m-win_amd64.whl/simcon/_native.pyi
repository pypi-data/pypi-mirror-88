import simcon._native
import typing

__all__ = [
    "EXCEPTION",
    "Message",
    "Msg",
    "MsgEvent",
    "MsgException",
    "MsgOpen",
    "MsgSimobjectData",
    "PERIOD",
    "RECV_ID",
    "Sim"
]


class EXCEPTION():
    """
    SimConnect Exception

    Members:

      NONE

      ERROR

      SIZE_MISMATCH

      UNRECOGNIZED_ID

      UNOPENED

      VERSION_MISMATCH

      TOO_MANY_GROUPS

      NAME_UNRECOGNIZED

      TOO_MANY_EVENT_NAMES

      EVENT_ID_DUPLICATE

      TOO_MANY_MAPS

      TOO_MANY_OBJECTS

      TOO_MANY_REQUESTS

      WEATHER_INVALID_PORT

      WEATHER_INVALID_METAR

      WEATHER_UNABLE_TO_GET_OBSERVATION

      WEATHER_UNABLE_TO_CREATE_STATION

      WEATHER_UNABLE_TO_REMOVE_STATION

      INVALID_DATA_TYPE

      INVALID_DATA_SIZE

      DATA_ERROR

      INVALID_ARRAY

      CREATE_OBJECT_FAILED

      LOAD_FLIGHTPLAN_FAILED

      OPERATION_INVALID_FOR_OBJECT_TYPE

      ILLEGAL_OPERATION

      ALREADY_SUBSCRIBED

      INVALID_ENUM

      DEFINITION_ERROR

      DUPLICATE_ID

      DATUM_ID

      OUT_OF_BOUNDS

      ALREADY_CREATED

      OBJECT_OUTSIDE_REALITY_BUBBLE

      OBJECT_CONTAINER

      OBJECT_AI

      OBJECT_ATC

      OBJECT_SCHEDULE
    """
    def __and__(self, other: object) -> object: ...
    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __gt__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __invert__(self) -> object: ...
    def __le__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __or__(self, other: object) -> object: ...
    def __rand__(self, other: object) -> object: ...
    def __repr__(self) -> str: ...
    def __ror__(self, other: object) -> object: ...
    def __rxor__(self, other: object) -> object: ...
    def __setstate__(self, state: int) -> None: ...
    def __xor__(self, other: object) -> object: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    ALREADY_CREATED: simcon._native.EXCEPTION # value = <EXCEPTION.ALREADY_CREATED: 32>
    ALREADY_SUBSCRIBED: simcon._native.EXCEPTION # value = <EXCEPTION.ALREADY_SUBSCRIBED: 26>
    CREATE_OBJECT_FAILED: simcon._native.EXCEPTION # value = <EXCEPTION.CREATE_OBJECT_FAILED: 22>
    DATA_ERROR: simcon._native.EXCEPTION # value = <EXCEPTION.DATA_ERROR: 20>
    DATUM_ID: simcon._native.EXCEPTION # value = <EXCEPTION.DATUM_ID: 30>
    DEFINITION_ERROR: simcon._native.EXCEPTION # value = <EXCEPTION.DEFINITION_ERROR: 28>
    DUPLICATE_ID: simcon._native.EXCEPTION # value = <EXCEPTION.DUPLICATE_ID: 29>
    ERROR: simcon._native.EXCEPTION # value = <EXCEPTION.ERROR: 1>
    EVENT_ID_DUPLICATE: simcon._native.EXCEPTION # value = <EXCEPTION.EVENT_ID_DUPLICATE: 9>
    ILLEGAL_OPERATION: simcon._native.EXCEPTION # value = <EXCEPTION.ILLEGAL_OPERATION: 25>
    INVALID_ARRAY: simcon._native.EXCEPTION # value = <EXCEPTION.INVALID_ARRAY: 21>
    INVALID_DATA_SIZE: simcon._native.EXCEPTION # value = <EXCEPTION.INVALID_DATA_SIZE: 19>
    INVALID_DATA_TYPE: simcon._native.EXCEPTION # value = <EXCEPTION.INVALID_DATA_TYPE: 18>
    INVALID_ENUM: simcon._native.EXCEPTION # value = <EXCEPTION.INVALID_ENUM: 27>
    LOAD_FLIGHTPLAN_FAILED: simcon._native.EXCEPTION # value = <EXCEPTION.LOAD_FLIGHTPLAN_FAILED: 23>
    NAME_UNRECOGNIZED: simcon._native.EXCEPTION # value = <EXCEPTION.NAME_UNRECOGNIZED: 7>
    NONE: simcon._native.EXCEPTION # value = <EXCEPTION.NONE: 0>
    OBJECT_AI: simcon._native.EXCEPTION # value = <EXCEPTION.OBJECT_AI: 35>
    OBJECT_ATC: simcon._native.EXCEPTION # value = <EXCEPTION.OBJECT_ATC: 36>
    OBJECT_CONTAINER: simcon._native.EXCEPTION # value = <EXCEPTION.OBJECT_CONTAINER: 34>
    OBJECT_OUTSIDE_REALITY_BUBBLE: simcon._native.EXCEPTION # value = <EXCEPTION.OBJECT_OUTSIDE_REALITY_BUBBLE: 33>
    OBJECT_SCHEDULE: simcon._native.EXCEPTION # value = <EXCEPTION.OBJECT_SCHEDULE: 37>
    OPERATION_INVALID_FOR_OBJECT_TYPE: simcon._native.EXCEPTION # value = <EXCEPTION.OPERATION_INVALID_FOR_OBJECT_TYPE: 24>
    OUT_OF_BOUNDS: simcon._native.EXCEPTION # value = <EXCEPTION.OUT_OF_BOUNDS: 31>
    SIZE_MISMATCH: simcon._native.EXCEPTION # value = <EXCEPTION.SIZE_MISMATCH: 2>
    TOO_MANY_EVENT_NAMES: simcon._native.EXCEPTION # value = <EXCEPTION.TOO_MANY_EVENT_NAMES: 8>
    TOO_MANY_GROUPS: simcon._native.EXCEPTION # value = <EXCEPTION.TOO_MANY_GROUPS: 6>
    TOO_MANY_MAPS: simcon._native.EXCEPTION # value = <EXCEPTION.TOO_MANY_MAPS: 10>
    TOO_MANY_OBJECTS: simcon._native.EXCEPTION # value = <EXCEPTION.TOO_MANY_OBJECTS: 11>
    TOO_MANY_REQUESTS: simcon._native.EXCEPTION # value = <EXCEPTION.TOO_MANY_REQUESTS: 12>
    UNOPENED: simcon._native.EXCEPTION # value = <EXCEPTION.UNOPENED: 4>
    UNRECOGNIZED_ID: simcon._native.EXCEPTION # value = <EXCEPTION.UNRECOGNIZED_ID: 3>
    VERSION_MISMATCH: simcon._native.EXCEPTION # value = <EXCEPTION.VERSION_MISMATCH: 5>
    WEATHER_INVALID_METAR: simcon._native.EXCEPTION # value = <EXCEPTION.WEATHER_INVALID_METAR: 14>
    WEATHER_INVALID_PORT: simcon._native.EXCEPTION # value = <EXCEPTION.WEATHER_INVALID_PORT: 13>
    WEATHER_UNABLE_TO_CREATE_STATION: simcon._native.EXCEPTION # value = <EXCEPTION.WEATHER_UNABLE_TO_CREATE_STATION: 16>
    WEATHER_UNABLE_TO_GET_OBSERVATION: simcon._native.EXCEPTION # value = <EXCEPTION.WEATHER_UNABLE_TO_GET_OBSERVATION: 15>
    WEATHER_UNABLE_TO_REMOVE_STATION: simcon._native.EXCEPTION # value = <EXCEPTION.WEATHER_UNABLE_TO_REMOVE_STATION: 17>
    __members__: dict # value = {'NONE': <EXCEPTION.NONE: 0>, 'ERROR': <EXCEPTION.ERROR: 1>, 'SIZE_MISMATCH': <EXCEPTION.SIZE_MISMATCH: 2>, 'UNRECOGNIZED_ID': <EXCEPTION.UNRECOGNIZED_ID: 3>, 'UNOPENED': <EXCEPTION.UNOPENED: 4>, 'VERSION_MISMATCH': <EXCEPTION.VERSION_MISMATCH: 5>, 'TOO_MANY_GROUPS': <EXCEPTION.TOO_MANY_GROUPS: 6>, 'NAME_UNRECOGNIZED': <EXCEPTION.NAME_UNRECOGNIZED: 7>, 'TOO_MANY_EVENT_NAMES': <EXCEPTION.TOO_MANY_EVENT_NAMES: 8>, 'EVENT_ID_DUPLICATE': <EXCEPTION.EVENT_ID_DUPLICATE: 9>, 'TOO_MANY_MAPS': <EXCEPTION.TOO_MANY_MAPS: 10>, 'TOO_MANY_OBJECTS': <EXCEPTION.TOO_MANY_OBJECTS: 11>, 'TOO_MANY_REQUESTS': <EXCEPTION.TOO_MANY_REQUESTS: 12>, 'WEATHER_INVALID_PORT': <EXCEPTION.WEATHER_INVALID_PORT: 13>, 'WEATHER_INVALID_METAR': <EXCEPTION.WEATHER_INVALID_METAR: 14>, 'WEATHER_UNABLE_TO_GET_OBSERVATION': <EXCEPTION.WEATHER_UNABLE_TO_GET_OBSERVATION: 15>, 'WEATHER_UNABLE_TO_CREATE_STATION': <EXCEPTION.WEATHER_UNABLE_TO_CREATE_STATION: 16>, 'WEATHER_UNABLE_TO_REMOVE_STATION': <EXCEPTION.WEATHER_UNABLE_TO_REMOVE_STATION: 17>, 'INVALID_DATA_TYPE': <EXCEPTION.INVALID_DATA_TYPE: 18>, 'INVALID_DATA_SIZE': <EXCEPTION.INVALID_DATA_SIZE: 19>, 'DATA_ERROR': <EXCEPTION.DATA_ERROR: 20>, 'INVALID_ARRAY': <EXCEPTION.INVALID_ARRAY: 21>, 'CREATE_OBJECT_FAILED': <EXCEPTION.CREATE_OBJECT_FAILED: 22>, 'LOAD_FLIGHTPLAN_FAILED': <EXCEPTION.LOAD_FLIGHTPLAN_FAILED: 23>, 'OPERATION_INVALID_FOR_OBJECT_TYPE': <EXCEPTION.OPERATION_INVALID_FOR_OBJECT_TYPE: 24>, 'ILLEGAL_OPERATION': <EXCEPTION.ILLEGAL_OPERATION: 25>, 'ALREADY_SUBSCRIBED': <EXCEPTION.ALREADY_SUBSCRIBED: 26>, 'INVALID_ENUM': <EXCEPTION.INVALID_ENUM: 27>, 'DEFINITION_ERROR': <EXCEPTION.DEFINITION_ERROR: 28>, 'DUPLICATE_ID': <EXCEPTION.DUPLICATE_ID: 29>, 'DATUM_ID': <EXCEPTION.DATUM_ID: 30>, 'OUT_OF_BOUNDS': <EXCEPTION.OUT_OF_BOUNDS: 31>, 'ALREADY_CREATED': <EXCEPTION.ALREADY_CREATED: 32>, 'OBJECT_OUTSIDE_REALITY_BUBBLE': <EXCEPTION.OBJECT_OUTSIDE_REALITY_BUBBLE: 33>, 'OBJECT_CONTAINER': <EXCEPTION.OBJECT_CONTAINER: 34>, 'OBJECT_AI': <EXCEPTION.OBJECT_AI: 35>, 'OBJECT_ATC': <EXCEPTION.OBJECT_ATC: 36>, 'OBJECT_SCHEDULE': <EXCEPTION.OBJECT_SCHEDULE: 37>}
    pass
class Message():
    def as_base(self) -> Msg: ...
    def as_event(self) -> MsgEvent: ...
    def as_exception(self) -> MsgException: ...
    def as_open(self) -> MsgOpen: ...
    def as_simobject_data(self) -> MsgSimobjectData: ...
    pass
class Msg():
    @property
    def dwID(self) -> int:
        """
        :type: int
        """
    @property
    def dwSize(self) -> int:
        """
        :type: int
        """
    @property
    def dwVersion(self) -> int:
        """
        :type: int
        """
    pass
class MsgEvent():
    @property
    def dwData(self) -> int:
        """
        :type: int
        """
    @property
    def uEventID(self) -> int:
        """
        :type: int
        """
    @property
    def uGroupID(self) -> int:
        """
        :type: int
        """
    pass
class MsgException():
    @property
    def dwException(self) -> int:
        """
        :type: int
        """
    @property
    def dwIndex(self) -> int:
        """
        :type: int
        """
    @property
    def dwSendID(self) -> int:
        """
        :type: int
        """
    pass
class MsgOpen():
    @property
    def dwApplicationBuildMajor(self) -> int:
        """
        :type: int
        """
    @property
    def dwApplicationBuildMinor(self) -> int:
        """
        :type: int
        """
    @property
    def dwApplicationVersionMajor(self) -> int:
        """
        :type: int
        """
    @property
    def dwApplicationVersionMinor(self) -> int:
        """
        :type: int
        """
    @property
    def dwSimConnectBuildMajor(self) -> int:
        """
        :type: int
        """
    @property
    def dwSimConnectBuildMinor(self) -> int:
        """
        :type: int
        """
    @property
    def dwSimConnectVersionMajor(self) -> int:
        """
        :type: int
        """
    @property
    def dwSimConnectVersionMinor(self) -> int:
        """
        :type: int
        """
    @property
    def szApplicationName(self) -> str:
        """
        :type: str
        """
    pass
class MsgSimobjectData():
    @property
    def data(self) -> bytes:
        """
        :type: bytes
        """
    @property
    def dwDefineID(self) -> int:
        """
        :type: int
        """
    @property
    def dwFlags(self) -> int:
        """
        :type: int
        """
    @property
    def dwObjectID(self) -> int:
        """
        :type: int
        """
    @property
    def dwRequestID(self) -> int:
        """
        :type: int
        """
    @property
    def dwentrynumber(self) -> int:
        """
        :type: int
        """
    @property
    def dwoutof(self) -> int:
        """
        :type: int
        """
    pass
class PERIOD():
    """
    Data request period

    Members:

      SIMCONNECT_PERIOD_NEVER

      SIMCONNECT_PERIOD_ONCE

      SIMCONNECT_PERIOD_VISUAL_FRAME

      SIMCONNECT_PERIOD_SIM_FRAME

      SIMCONNECT_PERIOD_SECOND
    """
    def __and__(self, other: object) -> object: ...
    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __gt__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __invert__(self) -> object: ...
    def __le__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __or__(self, other: object) -> object: ...
    def __rand__(self, other: object) -> object: ...
    def __repr__(self) -> str: ...
    def __ror__(self, other: object) -> object: ...
    def __rxor__(self, other: object) -> object: ...
    def __setstate__(self, state: int) -> None: ...
    def __xor__(self, other: object) -> object: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    SIMCONNECT_PERIOD_NEVER: simcon._native.PERIOD # value = <PERIOD.SIMCONNECT_PERIOD_NEVER: 0>
    SIMCONNECT_PERIOD_ONCE: simcon._native.PERIOD # value = <PERIOD.SIMCONNECT_PERIOD_ONCE: 1>
    SIMCONNECT_PERIOD_SECOND: simcon._native.PERIOD # value = <PERIOD.SIMCONNECT_PERIOD_SECOND: 4>
    SIMCONNECT_PERIOD_SIM_FRAME: simcon._native.PERIOD # value = <PERIOD.SIMCONNECT_PERIOD_SIM_FRAME: 3>
    SIMCONNECT_PERIOD_VISUAL_FRAME: simcon._native.PERIOD # value = <PERIOD.SIMCONNECT_PERIOD_VISUAL_FRAME: 2>
    __members__: dict # value = {'SIMCONNECT_PERIOD_NEVER': <PERIOD.SIMCONNECT_PERIOD_NEVER: 0>, 'SIMCONNECT_PERIOD_ONCE': <PERIOD.SIMCONNECT_PERIOD_ONCE: 1>, 'SIMCONNECT_PERIOD_VISUAL_FRAME': <PERIOD.SIMCONNECT_PERIOD_VISUAL_FRAME: 2>, 'SIMCONNECT_PERIOD_SIM_FRAME': <PERIOD.SIMCONNECT_PERIOD_SIM_FRAME: 3>, 'SIMCONNECT_PERIOD_SECOND': <PERIOD.SIMCONNECT_PERIOD_SECOND: 4>}
    pass
class RECV_ID():
    """
    Message type ID

    Members:

      NULL

      EXCEPTION

      OPEN

      QUIT

      EVENT

      EVENT_OBJECT_ADDREMOVE

      EVENT_FILENAME

      EVENT_FRAME

      SIMOBJECT_DATA

      SIMOBJECT_DATA_BYTYPE

      WEATHER_OBSERVATION

      CLOUD_STATE

      ASSIGNED_OBJECT_ID

      RESERVED_KEY

      CUSTOM_ACTION

      SYSTEM_STATE

      CLIENT_DATA

      EVENT_WEATHER_MODE

      AIRPORT_LIST

      VOR_LIST

      NDB_LIST

      WAYPOINT_LIST

      EVENT_MULTIPLAYER_SERVER_STARTED

      EVENT_MULTIPLAYER_CLIENT_STARTED

      EVENT_MULTIPLAYER_SESSION_ENDED

      EVENT_RACE_END

      EVENT_RACE_LAP
    """
    def __and__(self, other: object) -> object: ...
    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __gt__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __invert__(self) -> object: ...
    def __le__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __or__(self, other: object) -> object: ...
    def __rand__(self, other: object) -> object: ...
    def __repr__(self) -> str: ...
    def __ror__(self, other: object) -> object: ...
    def __rxor__(self, other: object) -> object: ...
    def __setstate__(self, state: int) -> None: ...
    def __xor__(self, other: object) -> object: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    AIRPORT_LIST: simcon._native.RECV_ID # value = <RECV_ID.AIRPORT_LIST: 18>
    ASSIGNED_OBJECT_ID: simcon._native.RECV_ID # value = <RECV_ID.ASSIGNED_OBJECT_ID: 12>
    CLIENT_DATA: simcon._native.RECV_ID # value = <RECV_ID.CLIENT_DATA: 16>
    CLOUD_STATE: simcon._native.RECV_ID # value = <RECV_ID.CLOUD_STATE: 11>
    CUSTOM_ACTION: simcon._native.RECV_ID # value = <RECV_ID.CUSTOM_ACTION: 14>
    EVENT: simcon._native.RECV_ID # value = <RECV_ID.EVENT: 4>
    EVENT_FILENAME: simcon._native.RECV_ID # value = <RECV_ID.EVENT_FILENAME: 6>
    EVENT_FRAME: simcon._native.RECV_ID # value = <RECV_ID.EVENT_FRAME: 7>
    EVENT_MULTIPLAYER_CLIENT_STARTED: simcon._native.RECV_ID # value = <RECV_ID.EVENT_MULTIPLAYER_CLIENT_STARTED: 23>
    EVENT_MULTIPLAYER_SERVER_STARTED: simcon._native.RECV_ID # value = <RECV_ID.EVENT_MULTIPLAYER_SERVER_STARTED: 22>
    EVENT_MULTIPLAYER_SESSION_ENDED: simcon._native.RECV_ID # value = <RECV_ID.EVENT_MULTIPLAYER_SESSION_ENDED: 24>
    EVENT_OBJECT_ADDREMOVE: simcon._native.RECV_ID # value = <RECV_ID.EVENT_OBJECT_ADDREMOVE: 5>
    EVENT_RACE_END: simcon._native.RECV_ID # value = <RECV_ID.EVENT_RACE_END: 25>
    EVENT_RACE_LAP: simcon._native.RECV_ID # value = <RECV_ID.EVENT_RACE_LAP: 26>
    EVENT_WEATHER_MODE: simcon._native.RECV_ID # value = <RECV_ID.EVENT_WEATHER_MODE: 17>
    EXCEPTION: simcon._native.RECV_ID # value = <RECV_ID.EXCEPTION: 1>
    NDB_LIST: simcon._native.RECV_ID # value = <RECV_ID.NDB_LIST: 20>
    NULL: simcon._native.RECV_ID # value = <RECV_ID.NULL: 0>
    OPEN: simcon._native.RECV_ID # value = <RECV_ID.OPEN: 2>
    QUIT: simcon._native.RECV_ID # value = <RECV_ID.QUIT: 3>
    RESERVED_KEY: simcon._native.RECV_ID # value = <RECV_ID.RESERVED_KEY: 13>
    SIMOBJECT_DATA: simcon._native.RECV_ID # value = <RECV_ID.SIMOBJECT_DATA: 8>
    SIMOBJECT_DATA_BYTYPE: simcon._native.RECV_ID # value = <RECV_ID.SIMOBJECT_DATA_BYTYPE: 9>
    SYSTEM_STATE: simcon._native.RECV_ID # value = <RECV_ID.SYSTEM_STATE: 15>
    VOR_LIST: simcon._native.RECV_ID # value = <RECV_ID.VOR_LIST: 19>
    WAYPOINT_LIST: simcon._native.RECV_ID # value = <RECV_ID.WAYPOINT_LIST: 21>
    WEATHER_OBSERVATION: simcon._native.RECV_ID # value = <RECV_ID.WEATHER_OBSERVATION: 10>
    __members__: dict # value = {'NULL': <RECV_ID.NULL: 0>, 'EXCEPTION': <RECV_ID.EXCEPTION: 1>, 'OPEN': <RECV_ID.OPEN: 2>, 'QUIT': <RECV_ID.QUIT: 3>, 'EVENT': <RECV_ID.EVENT: 4>, 'EVENT_OBJECT_ADDREMOVE': <RECV_ID.EVENT_OBJECT_ADDREMOVE: 5>, 'EVENT_FILENAME': <RECV_ID.EVENT_FILENAME: 6>, 'EVENT_FRAME': <RECV_ID.EVENT_FRAME: 7>, 'SIMOBJECT_DATA': <RECV_ID.SIMOBJECT_DATA: 8>, 'SIMOBJECT_DATA_BYTYPE': <RECV_ID.SIMOBJECT_DATA_BYTYPE: 9>, 'WEATHER_OBSERVATION': <RECV_ID.WEATHER_OBSERVATION: 10>, 'CLOUD_STATE': <RECV_ID.CLOUD_STATE: 11>, 'ASSIGNED_OBJECT_ID': <RECV_ID.ASSIGNED_OBJECT_ID: 12>, 'RESERVED_KEY': <RECV_ID.RESERVED_KEY: 13>, 'CUSTOM_ACTION': <RECV_ID.CUSTOM_ACTION: 14>, 'SYSTEM_STATE': <RECV_ID.SYSTEM_STATE: 15>, 'CLIENT_DATA': <RECV_ID.CLIENT_DATA: 16>, 'EVENT_WEATHER_MODE': <RECV_ID.EVENT_WEATHER_MODE: 17>, 'AIRPORT_LIST': <RECV_ID.AIRPORT_LIST: 18>, 'VOR_LIST': <RECV_ID.VOR_LIST: 19>, 'NDB_LIST': <RECV_ID.NDB_LIST: 20>, 'WAYPOINT_LIST': <RECV_ID.WAYPOINT_LIST: 21>, 'EVENT_MULTIPLAYER_SERVER_STARTED': <RECV_ID.EVENT_MULTIPLAYER_SERVER_STARTED: 22>, 'EVENT_MULTIPLAYER_CLIENT_STARTED': <RECV_ID.EVENT_MULTIPLAYER_CLIENT_STARTED: 23>, 'EVENT_MULTIPLAYER_SESSION_ENDED': <RECV_ID.EVENT_MULTIPLAYER_SESSION_ENDED: 24>, 'EVENT_RACE_END': <RECV_ID.EVENT_RACE_END: 25>, 'EVENT_RACE_LAP': <RECV_ID.EVENT_RACE_LAP: 26>}
    pass
class Sim():
    def __init__(self, arg0: str) -> None: ...
    def add_to_data_definition(self, arg0: int, arg1: str, arg2: str) -> None: ...
    def get_last_sent_packet_id(self) -> int: ...
    def interrupt_receive(self) -> None: ...
    def receive(self) -> Message: ...
    def request_data_on_sim_object(self, arg0: int, arg1: int, arg2: int, arg3: PERIOD) -> None: ...
    def request_data_on_sim_object_type(self, arg0: int, arg1: int) -> None: ...
    def subscribe_to_system_event(self, arg0: int, arg1: str) -> None: ...
    def unsubscribe_from_system_event(self, arg0: int) -> None: ...
    pass
