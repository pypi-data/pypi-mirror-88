#include <stdexcept>
#include <functional>
#include "sim.h"

void check_exc(HRESULT res) {
    if (res != 0) throw std::runtime_error(std::to_string(res));
};

Sim::Sim(const std::string &app_name) {
    hEventHandle = ::CreateEvent(nullptr, FALSE, FALSE, nullptr);
    check_exc(SimConnect_Open(&hSimConnect, app_name.c_str(), nullptr, 0, hEventHandle, SIMCONNECT_OPEN_CONFIGINDEX_LOCAL));
};

void Sim::add_to_data_definition(SIMCONNECT_DATA_DEFINITION_ID definition_id, const char* var, const char* units, SIMCONNECT_DATATYPE datum_type) const {
    check_exc(SimConnect_AddToDataDefinition(hSimConnect, definition_id, var, units, datum_type));
};

void Sim::request_data_on_sim_object_type(DWORD request_id, DWORD definition_id) const {
    SimConnect_RequestDataOnSimObjectType(hSimConnect, request_id, definition_id, 0, SIMCONNECT_SIMOBJECT_TYPE_USER);
}

void Sim::request_data_on_sim_object(DWORD request_id, DWORD definition_id, SIMCONNECT_OBJECT_ID object_type = SIMCONNECT_OBJECT_ID_USER, SIMCONNECT_PERIOD period = SIMCONNECT_PERIOD_SECOND) const {
    SimConnect_RequestDataOnSimObject(hSimConnect, request_id, definition_id, object_type, period);
};

void Sim::subscribe_to_system_event(SIMCONNECT_CLIENT_EVENT_ID event_id, const char *event_name) const {
    check_exc(SimConnect_SubscribeToSystemEvent(hSimConnect, event_id, event_name));
}

void Sim::unsubscribe_from_system_event(SIMCONNECT_CLIENT_EVENT_ID event_id) const {
    check_exc(SimConnect_UnsubscribeFromSystemEvent(hSimConnect, event_id));
}

DWORD Sim::get_last_sent_packet_id() const {
    DWORD packet_id;
    check_exc(SimConnect_GetLastSentPacketID(hSimConnect, &packet_id));
    return packet_id;
}

Sim::~Sim() {
    if (hSimConnect != nullptr) {
        SimConnect_Close(hSimConnect);
    }
};

void Sim::interrupt_receive() const {
    ::SetEvent(hEventHandle);
}

Message Sim::receive() const {
    SIMCONNECT_RECV *data = nullptr;
    DWORD cb_data;
    SimConnect_GetNextDispatch(hSimConnect, &data, &cb_data);
    if (data == nullptr) {
        ::WaitForSingleObject(hEventHandle, INFINITE);
        SimConnect_GetNextDispatch(hSimConnect, &data, &cb_data);
    }
    return Message(data);
}