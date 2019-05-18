import * as actionTypes from './actionTypes';


const fetchAssistants = () => {
    return {
        type: actionTypes.FETCH_ASSISTANTS_REQUEST
    };
};

const fetchAssistantsSuccess = (assistantList) => {
    return {
        type: actionTypes.FETCH_ASSISTANTS_SUCCESS,
        assistantList
    };
};

const fetchAssistantsFailure = (error) => {
    return {
        type: actionTypes.FETCH_ASSISTANTS_FAILURE,
        error
    };
};


const addAssistant = (newAssistant) => {
    return {
        type: actionTypes.ADD_ASSISTANT_REQUEST,
        newAssistant
    };
};

const addAssistantSuccess = (successMsg) => {
    return {
        type: actionTypes.ADD_ASSISTANT_SUCCESS,
        successMsg
    };
};

const addAssistantFailure = (error) => {
    return {
        type: actionTypes.ADD_ASSISTANT_FAILURE,
        error
    };
};

const updateAssistant = ({assistantID, updatedSettings}) => {
    return {
        type: actionTypes.UPDATE_ASSISTANT_REQUEST,
        assistantID,
        updatedSettings
    };
};

const updateAssistantSuccess = (successMsg) => {
    return {
        type: actionTypes.UPDATE_ASSISTANT_SUCCESS,
        successMsg
    };
};

const updateAssistantFailure = (error) => {
    return {
        type: actionTypes.UPDATE_ASSISTANT_FAILURE,
        error
    };
};



const deleteAssistant = (assistantID) => {
    return {
        type: actionTypes.DELETE_ASSISTANT_REQUEST,
        assistantID
    };
};

const deleteAssistantSuccess = (assistantID, successMsg) => {
    return {
        type: actionTypes.DELETE_ASSISTANT_SUCCESS,
        assistantID,
        successMsg
    };
};

const deleteAssistantFailure = (error) => {
    return {
        type: actionTypes.DELETE_ASSISTANT_FAILURE,
        error
    };
};


const changeAssistantStatus = (assistantID, status) => {
    return {
        type: actionTypes.CHANGE_ASSISTANT_STATUS_REQUEST,
        assistantID,
        status
    };
};

const changeAssistantStatusSuccess = (successMsg, status, assistantID) => {
    return {
        type: actionTypes.CHANGE_ASSISTANT_STATUS_SUCCESS,
        successMsg,
        status,
        assistantID
    };
};

const changeAssistantStatusFailure = (error) => {
    return {
        type: actionTypes.CHANGE_ASSISTANT_STATUS_FAILURE,
        error
    };
};


const updateFlow = (assistant) => {
    return {
        type: actionTypes.UPDATE_FLOW_REQUEST,
        assistant
    };
};

const updateFlowSuccess = (assistant, msg) => {
    return {
        type: actionTypes.UPDATE_FLOW_SUCCESS,
        assistant,
        msg
    };
};

const updateFlowFailure = (error) => {
    return {
        type: actionTypes.UPDATE_FLOW_FAILURE,
        error
    };
};

const selectAssistantCRM = (CRMID, assistantID) => {
    return {
        type: actionTypes.SELECT_ASSISTANT_CRM_REQUEST,
        CRMID,
        assistantID
    };
};

const selectAssistantCRMSuccess = (msg) => {
    return {
        type: actionTypes.SELECT_ASSISTANT_CRM_SUCCESS,
        msg
    };
};

const selectAssistantCRMFailure = (error) => {
    return {
        type: actionTypes.SELECT_ASSISTANT_CRM_FAILURE,
        error
    };
};

const resetAssistantCRM = (assistantID) => {
    return {
        type: actionTypes.RESET_ASSISTANT_CRM_REQUEST,
        assistantID
    };
};

const resetAssistantCRMSuccess = (msg) => {
    return {
        type: actionTypes.RESET_ASSISTANT_CRM_SUCCESS,
        msg
    };
};

const resetAssistantCRMFailure = (error) => {
    return {
        type: actionTypes.RESET_ASSISTANT_CRM_FAILURE,
        error
    };
};



export const assistantActions = {
    fetchAssistants,
    fetchAssistantsSuccess,
    fetchAssistantsFailure,

    addAssistant,
    addAssistantSuccess,
    addAssistantFailure,

    updateAssistant,
    updateAssistantSuccess,
    updateAssistantFailure,

    deleteAssistant,
    deleteAssistantSuccess,
    deleteAssistantFailure,

    changeAssistantStatus,
    changeAssistantStatusSuccess,
    changeAssistantStatusFailure,

    updateFlow,
    updateFlowSuccess,
    updateFlowFailure,

    selectAssistantCRM,
    selectAssistantCRMSuccess,
    selectAssistantCRMFailure,

    resetAssistantCRM,
    resetAssistantCRMSuccess,
    resetAssistantCRMFailure,

};
