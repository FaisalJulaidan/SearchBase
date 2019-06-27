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


const uploadLogo = (assistantID, file) => ({
    type: actionTypes.UPLOAD_LOGO_REQUEST,
    assistantID,
    file
});

const uploadLogoSuccess = (msg) => ({
    type: actionTypes.UPLOAD_LOGO_SUCCESS,
    msg
});

const uploadLogoFailure = (error) => ({
    type: actionTypes.UPLOAD_LOGO_FAILURE,
    error
});


const deleteLogo = (assistantID) => ({
    type: actionTypes.DELETE_LOGO_REQUEST,
    assistantID
});

const deleteLogoSuccess = (msg) => ({
    type: actionTypes.DELETE_LOGO_SUCCESS,
    msg
});

const deleteLogoFailure = (error) => ({
    type: actionTypes.DELETE_LOGO_FAILURE,
    error
});

const connectAssistantCRM = (CRMID, assistantID) => ({
    type: actionTypes.CONNECT_ASSISTANT_MARKETPLACE_REQUEST,
    CRMID,
    assistantID
});

const connectAssistantCRMSuccess = (CRMID, msg) => ({
    type: actionTypes.CONNECT_ASSISTANT_MARKETPLACE_SUCCESS,
    CRMID,
    msg
});

const connectAssistantCRMFailure = (error) => ({
    type: actionTypes.CONNECT_ASSISTANT_MARKETPLACE_FAILURE,
    error
});

// Connections
const disconnectAssistantCRM = (assistantID) => ({
    type: actionTypes.DISCONNECT_ASSISTANT_MARKETPLACE_REQUEST,
    assistantID
});

const disconnectAssistantCRMSuccess = (msg) => ({
    type: actionTypes.DISCONNECT_ASSISTANT_MARKETPLACE_SUCCESS,
    msg
});

const disconnectAssistantCRMFailure = (error) => ({
    type: actionTypes.DISCONNECT_ASSISTANT_MARKETPLACE_FAILURE,
    error
});

const connectAutoPilot = (autoPilotID, assistantID) => ({
    type: actionTypes.CONNECT_ASSISTANT_AUTO_PILOT_REQUEST,
    assistantID,
    autoPilotID
});

const connectAutoPilotSuccess = (autoPilotID) => ({
    type: actionTypes.CONNECT_ASSISTANT_AUTO_PILOT_SUCCESS,
    autoPilotID
});

const connectAutoPilotFailure = (error) => ({
    type: actionTypes.CONNECT_ASSISTANT_AUTO_PILOT_FAILURE,
    error
});

const disconnectAutoPilot = (assistantID) => ({
    type: actionTypes.DISCONNECT_ASSISTANT_AUTO_PILOT_REQUEST,
    assistantID,
});

const disconnectAutoPilotSuccess = (msg) => ({
    type: actionTypes.DISCONNECT_ASSISTANT_AUTO_PILOT_SUCCESS,
    msg
});

const disconnectAutoPilotFailure = (error) => ({
    type: actionTypes.DISCONNECT_ASSISTANT_AUTO_PILOT_FAILURE,
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

    connectAssistantCRM,
    connectAssistantCRMSuccess,
    connectAssistantCRMFailure,

    disconnectAssistantCRM,
    disconnectAssistantCRMSuccess,
    disconnectAssistantCRMFailure,

    uploadLogo,
    uploadLogoSuccess,
    uploadLogoFailure,

    deleteLogo,
    deleteLogoSuccess,
    deleteLogoFailure,

    connectAutoPilot,
    connectAutoPilotSuccess,
    connectAutoPilotFailure,

    disconnectAutoPilot,
    disconnectAutoPilotSuccess,
    disconnectAutoPilotFailure,
};
