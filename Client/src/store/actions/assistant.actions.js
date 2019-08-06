import * as actionTypes from './actionTypes';


const fetchAssistants = () => ({
    type: actionTypes.FETCH_ASSISTANTS_REQUEST
});

const fetchAssistantsSuccess = (assistantList) => ({
    type: actionTypes.FETCH_ASSISTANTS_SUCCESS,
    assistantList
});

const fetchAssistantsFailure = (error) => ({
    type: actionTypes.FETCH_ASSISTANTS_FAILURE,
    error
});


const fetchAssistant = (assistantID) => ({
    type: actionTypes.FETCH_ASSISTANT_REQUEST,
    meta: {thunk: true},
    assistantID
});

const fetchAssistantSuccess = (assistant) => ({
    type: actionTypes.FETCH_ASSISTANT_SUCCESS,
    assistant
});

const fetchAssistantFailure = (error) => ({
    type: actionTypes.FETCH_ASSISTANT_FAILURE,
    error
});


const addAssistant = (newAssistant) => ({
    type: actionTypes.ADD_ASSISTANT_REQUEST,
    newAssistant
});

const addAssistantSuccess = (newAssistant, successMsg) => ({
    type: actionTypes.ADD_ASSISTANT_SUCCESS,
    newAssistant,
    successMsg
});

const addAssistantFailure = (error) => ({
    type: actionTypes.ADD_ASSISTANT_FAILURE,
    error
});

const updateAssistant = (assistantID, updatedSettings) => ({
    type: actionTypes.UPDATE_ASSISTANT_REQUEST,
    assistantID,
    updatedSettings
});

const updateAssistantSuccess = (assistantID, updatedAssistant, successMsg) => ({
    type: actionTypes.UPDATE_ASSISTANT_SUCCESS,
    assistantID,
    updatedAssistant,
    successMsg
});

const updateAssistantFailure = (error) => ({
    type: actionTypes.UPDATE_ASSISTANT_FAILURE,
    error
});


const updateAssistantConfigs = (assistantID, updatedSettings) => ({
    type: actionTypes.UPDATE_ASSISTANT_CONFIGS_REQUEST,
    assistantID,
    updatedSettings
});

const updateAssistantConfigsSuccess = (assistantID, updatedAssistant, successMsg) => ({
    type: actionTypes.UPDATE_ASSISTANT_CONFIGS_SUCCESS,
    assistantID,
    updatedAssistant,
    successMsg
});

const updateAssistantConfigsFailure = (error) => ({
    type: actionTypes.UPDATE_ASSISTANT_CONFIGS_FAILURE,
    error
});


const deleteAssistant = (assistantID) => ({
    type: actionTypes.DELETE_ASSISTANT_REQUEST,
    meta: {thunk: true},
    assistantID
});

const deleteAssistantSuccess = (assistantID, successMsg) => ({
    type: actionTypes.DELETE_ASSISTANT_SUCCESS,
    assistantID,
    successMsg
});

const deleteAssistantFailure = (error) => ({
    type: actionTypes.DELETE_ASSISTANT_FAILURE,
    error
});


const changeAssistantStatus = (assistantID, status) => ({
    type: actionTypes.CHANGE_ASSISTANT_STATUS_REQUEST,
    assistantID,
    status
});

const changeAssistantStatusSuccess = (successMsg, status, assistantID) => ({
    type: actionTypes.CHANGE_ASSISTANT_STATUS_SUCCESS,
    successMsg,
    status,
    assistantID
});

const changeAssistantStatusFailure = (error) => ({
    type: actionTypes.CHANGE_ASSISTANT_STATUS_FAILURE,
    error
});


const updateFlow = (assistant) => ({
    type: actionTypes.UPDATE_FLOW_REQUEST,
    meta: {thunk: true},
    assistant
});

const updateFlowSuccess = (assistant, msg) => ({
    type: actionTypes.UPDATE_FLOW_SUCCESS,
    assistant,
    msg
});

const updateFlowFailure = (error) => ({
    type: actionTypes.UPDATE_FLOW_FAILURE,
    error
});


// === Connections ===
// CRM
const connectToCRM = (CRMID, assistantID) => ({
    type: actionTypes.CONNECT_ASSISTANT_TO_CRM_REQUEST,
    CRMID,
    assistantID
});

const connectToCRMSuccess = (CRMID, msg) => ({
    type: actionTypes.CONNECT_ASSISTANT_TO_CRM_SUCCESS,
    CRMID,
    msg
});

const connectToCRMFailure = (error) => ({
    type: actionTypes.CONNECT_ASSISTANT_TO_CRM_FAILURE,
    error
});


const disconnectFromCRM = (assistantID) => ({
    type: actionTypes.DISCONNECT_ASSISTANT_FROM_CRM_REQUEST,
    assistantID
});

const disconnectFromCRMSuccess = (msg) => ({
    type: actionTypes.DISCONNECT_ASSISTANT_FROM_CRM_SUCCESS,
    msg
});

const disconnectFromCRMFailure = (error) => ({
    type: actionTypes.DISCONNECT_ASSISTANT_FROM_CRM_FAILURE,
    error
});


// Calendar
const connectToCalendar = (calendarID, assistantID) => ({
    type: actionTypes.CONNECT_ASSISTANT_TO_CALENDAR_REQUEST,
    calendarID,
    assistantID
});

const connectToCalendarSuccess = (calendarID, msg) => ({
    type: actionTypes.CONNECT_ASSISTANT_TO_CALENDAR_SUCCESS,
    calendarID,
    msg
});

const connectToCalendarFailure = (error) => ({
    type: actionTypes.CONNECT_ASSISTANT_TO_CALENDAR_FAILURE,
    error
});


const disconnectFromCalendar = (assistantID) => ({
    type: actionTypes.DISCONNECT_ASSISTANT_FROM_CALENDAR_REQUEST,
    assistantID
});

const disconnectFromCalendarSuccess = (msg) => ({
    type: actionTypes.DISCONNECT_ASSISTANT_FROM_CALENDAR_SUCCESS,
    msg
});

const disconnectFromCalendarFailure = (error) => ({
    type: actionTypes.DISCONNECT_ASSISTANT_FROM_CALENDAR_FAILURE,
    error
});



// Messenger
const connectToMessenger = (messengerID, assistantID) => ({
    type: actionTypes.CONNECT_ASSISTANT_TO_MESSENGER_REQUEST,
    assistantID,
    messengerID
});

const connectToMessengerSuccess = (messengerID) => ({
    type: actionTypes.CONNECT_ASSISTANT_TO_MESSENGER_SUCCESS,
    messengerID
});

const connectToMessengerFailure = (error) => ({
    type: actionTypes.CONNECT_ASSISTANT_TO_MESSENGER_FAILURE,
    error
});

const disconnectFromMessenger = (assistantID) => ({
    type: actionTypes.DISCONNECT_ASSISTANT_FROM_MESSENGER_REQUEST,
    assistantID,
});

const disconnectFromMessengerSuccess = (msg) => ({
    type: actionTypes.DISCONNECT_ASSISTANT_FROM_MESSENGER_SUCCESS,
    msg
});

const disconnectFromMessengerFailure = (error) => ({
    type: actionTypes.DISCONNECT_ASSISTANT_FROM_MESSENGER_FAILURE,
    error
});


// Auto Pilot
const connectToAutoPilot = (autoPilotID, assistantID) => ({
    type: actionTypes.CONNECT_ASSISTANT_TO_AUTO_PILOT_REQUEST,
    assistantID,
    autoPilotID
});

const connectToAutoPilotSuccess = (autoPilotID) => ({
    type: actionTypes.CONNECT_ASSISTANT_TO_AUTO_PILOT_SUCCESS,
    autoPilotID
});

const connectToAutoPilotFailure = (error) => ({
    type: actionTypes.CONNECT_ASSISTANT_TO_AUTO_PILOT_FAILURE,
    error
});

const disconnectFromAutoPilot = (assistantID) => ({
    type: actionTypes.DISCONNECT_ASSISTANT_FROM_AUTO_PILOT_REQUEST,
    assistantID,
});

const disconnectFromAutoPilotSuccess = (msg) => ({
    type: actionTypes.DISCONNECT_ASSISTANT_FROM_AUTO_PILOT_SUCCESS,
    msg
});

const disconnectFromAutoPilotFailure = (error) => ({
    type: actionTypes.DISCONNECT_ASSISTANT_FROM_AUTO_PILOT_FAILURE,
    error
});


export const assistantActions = {
    fetchAssistants,
    fetchAssistantsSuccess,
    fetchAssistantsFailure,

    fetchAssistant,
    fetchAssistantSuccess,
    fetchAssistantFailure,

    addAssistant,
    addAssistantSuccess,
    addAssistantFailure,

    updateAssistant,
    updateAssistantSuccess,
    updateAssistantFailure,

    updateAssistantConfigs,
    updateAssistantConfigsSuccess,
    updateAssistantConfigsFailure,

    deleteAssistant,
    deleteAssistantSuccess,
    deleteAssistantFailure,

    changeAssistantStatus,
    changeAssistantStatusSuccess,
    changeAssistantStatusFailure,

    updateFlow,
    updateFlowSuccess,
    updateFlowFailure,

    connectToCRM,
    connectToCRMSuccess,
    connectToCRMFailure,

    disconnectFromCRM,
    disconnectFromCRMSuccess,
    disconnectFromCRMFailure,

    connectToCalendar,
    connectToCalendarSuccess,
    connectToCalendarFailure,

    disconnectFromCalendar,
    disconnectFromCalendarSuccess,
    disconnectFromCalendarFailure,

    connectToMessenger,
    connectToMessengerSuccess,
    connectToMessengerFailure,

    disconnectFromMessenger,
    disconnectFromMessengerSuccess,
    disconnectFromMessengerFailure,

    connectToAutoPilot,
    connectToAutoPilotSuccess,
    connectToAutoPilotFailure,

    disconnectFromAutoPilot,
    disconnectFromAutoPilotSuccess,
    disconnectFromAutoPilotFailure,
};
