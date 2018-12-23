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



const changeAssistantStatus = (assistantID) => {
    return {
        type: actionTypes.CHANGE_ASSISTANT_STATUS_REQUEST,
        assistantID
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

export const assistantActions = {
    fetchAssistants,
    fetchAssistantsSuccess,
    fetchAssistantsFailure,
    addAssistant,
    addAssistantSuccess,
    addAssistantFailure,

    changeAssistantStatus,
    changeAssistantStatusSuccess,
    changeAssistantStatusFailure,
};