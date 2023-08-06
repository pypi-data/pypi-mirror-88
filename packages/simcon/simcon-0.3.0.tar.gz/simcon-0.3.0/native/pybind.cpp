#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "sim.h"

HRESULT h;

namespace py = pybind11;

PYBIND11_MODULE(_native, m) {
    py::enum_<SIMCONNECT_EXCEPTION>(m, "EXCEPTION", py::arithmetic(), "SimConnect Exception")
    .value("NONE", SIMCONNECT_EXCEPTION_NONE)
    .value("ERROR", SIMCONNECT_EXCEPTION_ERROR)
    .value("SIZE_MISMATCH", SIMCONNECT_EXCEPTION_SIZE_MISMATCH)
    .value("UNRECOGNIZED_ID", SIMCONNECT_EXCEPTION_UNRECOGNIZED_ID)
    .value("UNOPENED", SIMCONNECT_EXCEPTION_UNOPENED)
    .value("VERSION_MISMATCH", SIMCONNECT_EXCEPTION_VERSION_MISMATCH)
    .value("TOO_MANY_GROUPS", SIMCONNECT_EXCEPTION_TOO_MANY_GROUPS)
    .value("NAME_UNRECOGNIZED", SIMCONNECT_EXCEPTION_NAME_UNRECOGNIZED)
    .value("TOO_MANY_EVENT_NAMES", SIMCONNECT_EXCEPTION_TOO_MANY_EVENT_NAMES)
    .value("EVENT_ID_DUPLICATE", SIMCONNECT_EXCEPTION_EVENT_ID_DUPLICATE)
    .value("TOO_MANY_MAPS", SIMCONNECT_EXCEPTION_TOO_MANY_MAPS)
    .value("TOO_MANY_OBJECTS", SIMCONNECT_EXCEPTION_TOO_MANY_OBJECTS)
    .value("TOO_MANY_REQUESTS", SIMCONNECT_EXCEPTION_TOO_MANY_REQUESTS)
    .value("WEATHER_INVALID_PORT", SIMCONNECT_EXCEPTION_WEATHER_INVALID_PORT)
    .value("WEATHER_INVALID_METAR", SIMCONNECT_EXCEPTION_WEATHER_INVALID_METAR)
    .value("WEATHER_UNABLE_TO_GET_OBSERVATION", SIMCONNECT_EXCEPTION_WEATHER_UNABLE_TO_GET_OBSERVATION)
    .value("WEATHER_UNABLE_TO_CREATE_STATION", SIMCONNECT_EXCEPTION_WEATHER_UNABLE_TO_CREATE_STATION)
    .value("WEATHER_UNABLE_TO_REMOVE_STATION", SIMCONNECT_EXCEPTION_WEATHER_UNABLE_TO_REMOVE_STATION)
    .value("INVALID_DATA_TYPE", SIMCONNECT_EXCEPTION_INVALID_DATA_TYPE)
    .value("INVALID_DATA_SIZE", SIMCONNECT_EXCEPTION_INVALID_DATA_SIZE)
    .value("DATA_ERROR", SIMCONNECT_EXCEPTION_DATA_ERROR)
    .value("INVALID_ARRAY", SIMCONNECT_EXCEPTION_INVALID_ARRAY)
    .value("CREATE_OBJECT_FAILED", SIMCONNECT_EXCEPTION_CREATE_OBJECT_FAILED)
    .value("LOAD_FLIGHTPLAN_FAILED", SIMCONNECT_EXCEPTION_LOAD_FLIGHTPLAN_FAILED)
    .value("OPERATION_INVALID_FOR_OBJECT_TYPE", SIMCONNECT_EXCEPTION_OPERATION_INVALID_FOR_OBJECT_TYPE)
    .value("ILLEGAL_OPERATION", SIMCONNECT_EXCEPTION_ILLEGAL_OPERATION)
    .value("ALREADY_SUBSCRIBED", SIMCONNECT_EXCEPTION_ALREADY_SUBSCRIBED)
    .value("INVALID_ENUM", SIMCONNECT_EXCEPTION_INVALID_ENUM)
    .value("DEFINITION_ERROR", SIMCONNECT_EXCEPTION_DEFINITION_ERROR)
    .value("DUPLICATE_ID", SIMCONNECT_EXCEPTION_DUPLICATE_ID)
    .value("DATUM_ID", SIMCONNECT_EXCEPTION_DATUM_ID)
    .value("OUT_OF_BOUNDS", SIMCONNECT_EXCEPTION_OUT_OF_BOUNDS)
    .value("ALREADY_CREATED", SIMCONNECT_EXCEPTION_ALREADY_CREATED)
    .value("OBJECT_OUTSIDE_REALITY_BUBBLE", SIMCONNECT_EXCEPTION_OBJECT_OUTSIDE_REALITY_BUBBLE)
    .value("OBJECT_CONTAINER", SIMCONNECT_EXCEPTION_OBJECT_CONTAINER)
    .value("OBJECT_AI", SIMCONNECT_EXCEPTION_OBJECT_AI)
    .value("OBJECT_ATC", SIMCONNECT_EXCEPTION_OBJECT_ATC)
    .value("OBJECT_SCHEDULE", SIMCONNECT_EXCEPTION_OBJECT_SCHEDULE)
    ;

    py::enum_<SIMCONNECT_RECV_ID>(m, "RECV_ID", py::arithmetic(), "Message type ID")
    .value("NULL", SIMCONNECT_RECV_ID_NULL)
    .value("EXCEPTION", SIMCONNECT_RECV_ID_EXCEPTION)
    .value("OPEN", SIMCONNECT_RECV_ID_OPEN)
    .value("QUIT", SIMCONNECT_RECV_ID_QUIT)
    .value("EVENT", SIMCONNECT_RECV_ID_EVENT)
    .value("EVENT_OBJECT_ADDREMOVE", SIMCONNECT_RECV_ID_EVENT_OBJECT_ADDREMOVE)
    .value("EVENT_FILENAME", SIMCONNECT_RECV_ID_EVENT_FILENAME)
    .value("EVENT_FRAME", SIMCONNECT_RECV_ID_EVENT_FRAME)
    .value("SIMOBJECT_DATA", SIMCONNECT_RECV_ID_SIMOBJECT_DATA)
    .value("SIMOBJECT_DATA_BYTYPE", SIMCONNECT_RECV_ID_SIMOBJECT_DATA_BYTYPE)
    .value("WEATHER_OBSERVATION", SIMCONNECT_RECV_ID_WEATHER_OBSERVATION)
    .value("CLOUD_STATE", SIMCONNECT_RECV_ID_CLOUD_STATE)
    .value("ASSIGNED_OBJECT_ID", SIMCONNECT_RECV_ID_ASSIGNED_OBJECT_ID)
    .value("RESERVED_KEY", SIMCONNECT_RECV_ID_RESERVED_KEY)
    .value("CUSTOM_ACTION", SIMCONNECT_RECV_ID_CUSTOM_ACTION)
    .value("SYSTEM_STATE", SIMCONNECT_RECV_ID_SYSTEM_STATE)
    .value("CLIENT_DATA", SIMCONNECT_RECV_ID_CLIENT_DATA)
    .value("EVENT_WEATHER_MODE", SIMCONNECT_RECV_ID_EVENT_WEATHER_MODE)
    .value("AIRPORT_LIST", SIMCONNECT_RECV_ID_AIRPORT_LIST)
    .value("VOR_LIST", SIMCONNECT_RECV_ID_VOR_LIST)
    .value("NDB_LIST", SIMCONNECT_RECV_ID_NDB_LIST)
    .value("WAYPOINT_LIST", SIMCONNECT_RECV_ID_WAYPOINT_LIST)
    .value("EVENT_MULTIPLAYER_SERVER_STARTED", SIMCONNECT_RECV_ID_EVENT_MULTIPLAYER_SERVER_STARTED)
    .value("EVENT_MULTIPLAYER_CLIENT_STARTED", SIMCONNECT_RECV_ID_EVENT_MULTIPLAYER_CLIENT_STARTED)
    .value("EVENT_MULTIPLAYER_SESSION_ENDED", SIMCONNECT_RECV_ID_EVENT_MULTIPLAYER_SESSION_ENDED)
    .value("EVENT_RACE_END", SIMCONNECT_RECV_ID_EVENT_RACE_END)
    .value("EVENT_RACE_LAP", SIMCONNECT_RECV_ID_EVENT_RACE_LAP)
    ;

    py::enum_<SIMCONNECT_PERIOD>(m, "PERIOD", py::arithmetic(), "Data request period")
    .value("NEVER", SIMCONNECT_PERIOD_NEVER)  // FIXME: Remove SIMCONNECT_PERIOD_ prefix
    .value("ONCE", SIMCONNECT_PERIOD_ONCE)
    .value("VISUAL_FRAME", SIMCONNECT_PERIOD_VISUAL_FRAME)
    .value("SIM_FRAME", SIMCONNECT_PERIOD_SIM_FRAME)
    .value("SECOND", SIMCONNECT_PERIOD_SECOND)
    ;

    py::enum_<SIMCONNECT_DATATYPE>(m, "DATATYPE", py::arithmetic(), "Data type")
    .value("INVALID", SIMCONNECT_DATATYPE_INVALID)
    .value("INT32", SIMCONNECT_DATATYPE_INT32)
    .value("INT64", SIMCONNECT_DATATYPE_INT64)
    .value("FLOAT32", SIMCONNECT_DATATYPE_FLOAT32)
    .value("FLOAT64", SIMCONNECT_DATATYPE_FLOAT64)
    .value("STRING8", SIMCONNECT_DATATYPE_STRING8)
    .value("STRING32", SIMCONNECT_DATATYPE_STRING32)
    .value("STRING64", SIMCONNECT_DATATYPE_STRING64)
    .value("STRING128", SIMCONNECT_DATATYPE_STRING128)
    .value("STRING256", SIMCONNECT_DATATYPE_STRING256)
    .value("STRING260", SIMCONNECT_DATATYPE_STRING260)
    .value("STRINGV", SIMCONNECT_DATATYPE_STRINGV)
    .value("INITPOSITION", SIMCONNECT_DATATYPE_INITPOSITION)
    .value("MARKERSTATE", SIMCONNECT_DATATYPE_MARKERSTATE)
    .value("WAYPOINT", SIMCONNECT_DATATYPE_WAYPOINT)
    .value("LATLONALT", SIMCONNECT_DATATYPE_LATLONALT)
    .value("XYZ", SIMCONNECT_DATATYPE_XYZ)
    ;

    py::class_<SIMCONNECT_RECV, std::shared_ptr<SIMCONNECT_RECV>>(m, "Msg")
    .def_readonly("dwSize", &SIMCONNECT_RECV::dwSize)
    .def_readonly("dwVersion", &SIMCONNECT_RECV::dwVersion)
    .def_readonly("dwID", &SIMCONNECT_RECV::dwID)
    ;

    py::class_<SIMCONNECT_RECV_OPEN, std::shared_ptr<SIMCONNECT_RECV_OPEN>>(m, "MsgOpen")
    .def_readonly("szApplicationName", &SIMCONNECT_RECV_OPEN::szApplicationName)
    .def_readonly("dwApplicationVersionMajor", &SIMCONNECT_RECV_OPEN::dwApplicationVersionMajor)
    .def_readonly("dwApplicationVersionMinor", &SIMCONNECT_RECV_OPEN::dwApplicationVersionMinor)
    .def_readonly("dwApplicationBuildMajor", &SIMCONNECT_RECV_OPEN::dwApplicationBuildMajor)
    .def_readonly("dwApplicationBuildMinor", &SIMCONNECT_RECV_OPEN::dwApplicationBuildMinor)
    .def_readonly("dwSimConnectVersionMajor", &SIMCONNECT_RECV_OPEN::dwSimConnectVersionMajor)
    .def_readonly("dwSimConnectVersionMinor", &SIMCONNECT_RECV_OPEN::dwSimConnectVersionMinor)
    .def_readonly("dwSimConnectBuildMajor", &SIMCONNECT_RECV_OPEN::dwSimConnectBuildMajor)
    .def_readonly("dwSimConnectBuildMinor", &SIMCONNECT_RECV_OPEN::dwSimConnectBuildMinor)
    ;
    
    py::class_<SIMCONNECT_RECV_EXCEPTION, std::shared_ptr<SIMCONNECT_RECV_EXCEPTION>>(m, "MsgException")
    .def_readonly("dwException", &SIMCONNECT_RECV_EXCEPTION::dwException)
    .def_readonly("dwSendID", &SIMCONNECT_RECV_EXCEPTION::dwSendID)
    .def_readonly("dwIndex", &SIMCONNECT_RECV_EXCEPTION::dwIndex)
    ;
    
    py::class_<SIMCONNECT_RECV_EVENT, std::shared_ptr<SIMCONNECT_RECV_EVENT>>(m, "MsgEvent")
    .def_readonly("uGroupID", &SIMCONNECT_RECV_EVENT::uGroupID)
    .def_readonly("uEventID", &SIMCONNECT_RECV_EVENT::uEventID)
    .def_readonly("dwData", &SIMCONNECT_RECV_EVENT::dwData)
    ;

    py::class_<SIMCONNECT_RECV_SIMOBJECT_DATA, std::shared_ptr<SIMCONNECT_RECV_SIMOBJECT_DATA>>(m, "MsgSimobjectData")
    .def_readonly("dwRequestID", &SIMCONNECT_RECV_SIMOBJECT_DATA::dwRequestID)
    .def_readonly("dwObjectID", &SIMCONNECT_RECV_SIMOBJECT_DATA::dwObjectID)
    .def_readonly("dwDefineID", &SIMCONNECT_RECV_SIMOBJECT_DATA::dwDefineID)
    .def_readonly("dwFlags", &SIMCONNECT_RECV_SIMOBJECT_DATA::dwFlags)
    .def_readonly("dwentrynumber", &SIMCONNECT_RECV_SIMOBJECT_DATA::dwentrynumber)
    .def_readonly("dwoutof", &SIMCONNECT_RECV_SIMOBJECT_DATA::dwoutof)
    //.def_readonly("dwDefineCount", &SIMCONNECT_RECV_SIMOBJECT_DATA::dwDefineCount)
    //.def_readonly("dwData", &SIMCONNECT_RECV_SIMOBJECT_DATA::dwData)
    .def(
        "get_bytes",
        [](const SIMCONNECT_RECV_SIMOBJECT_DATA &d, size_t size) {
            return py::bytes((char*)&d.dwData, size);
        }
    )
    ;
    
    py::class_<Message>(m, "Message")
    .def("as_base", &Message::as_base)
    .def("as_exception", &Message::as_exception)
    .def("as_open", &Message::as_open)
    .def("as_event", &Message::as_event)
    .def("as_simobject_data", &Message::as_simobject_data)
    ;

    py::class_<Sim>(m, "Sim")
    .def(py::init<const std::string&>())
    .def("add_to_data_definition", &Sim::add_to_data_definition)
    .def("request_data_on_sim_object_type", &Sim::request_data_on_sim_object_type)
    .def("request_data_on_sim_object", &Sim::request_data_on_sim_object)
    .def("subscribe_to_system_event", &Sim::subscribe_to_system_event)
    .def("unsubscribe_from_system_event", &Sim::unsubscribe_from_system_event)
    .def("get_last_sent_packet_id", &Sim::get_last_sent_packet_id)
    .def("receive", &Sim::receive, py::call_guard<py::gil_scoped_release>())
    .def("interrupt_receive", &Sim::interrupt_receive)
    ;
}