import * as actionTypes from './actionTypes';

// Fetch
const fetchAutoPilots = () => {
    return {
        type: actionTypes.FETCH_AUTOPILOTS_REQUEST
    };
};

const fetchAutoPilotsSuccess = (autoPilotsList) => {
    return {
        type: actionTypes.FETCH_AUTOPILOTS_SUCCESS,
        autoPilotsList
    };
};

const fetchAutoPilotsFailure = (errorMsg) => {
    return {
        type: actionTypes.FETCH_AUTOPILOTS_FAILURE,
        errorMsg
    };
};


// Add
const addAutoPilot = (newAutoPilot) => {
    return {
        type: actionTypes.ADD_AUTOPILOT_REQUEST,
        newAutoPilot
    };
};

const addAutoPilotSuccess = (newAutoPilot, successMsg) => {
    return {
        type: actionTypes.ADD_AUTOPILOT_SUCCESS,
        newAutoPilot,
        successMsg
    };
};

const addAutoPilotFailure = (errorMsg) => {
    return {
        type: actionTypes.ADD_AUTOPILOT_FAILURE,
        errorMsg
    };
};


// Update
const updateAutoPilot = (autoPilotID, updatedValues) => {
    return {
        type: actionTypes.UPDATE_AUTOPILOT_REQUEST,
        autoPilotID,
        updatedValues
    };
};

const updateAutoPilotSuccess = (autoPilotID, updatedAutoPilot, successMsg) => {
    return {
        type: actionTypes.UPDATE_AUTOPILOT_SUCCESS,
        autoPilotID,
        updatedAutoPilot,
        successMsg
    };
};

const updateAutoPilotFailure = (errorMsg) => {
    return {
        type: actionTypes.UPDATE_AUTOPILOT_FAILURE,
        errorMsg
    };
};


// Delete
const deleteAutoPilot = (authPilotID) => {
    return {
        type: actionTypes.DELETE_AUTOPILOT_REQUEST,
        authPilotID,
    };
};

const deleteAutoPilotSuccess = (authPilotID, successMsg) => {
    return {
        type: actionTypes.DELETE_AUTOPILOT_SUCCESS,
        authPilotID,
        successMsg
    };
};

const deleteAutoPilotFailure = (errorMsg) => {
    return {
        type: actionTypes.DELETE_AUTOPILOT_FAILURE,
        errorMsg
    };
};




export const autoPilotActions = {
    fetchAutoPilots,
    fetchAutoPilotsSuccess,
    fetchAutoPilotsFailure,

    addAutoPilot,
    addAutoPilotSuccess,
    addAutoPilotFailure,

    updateAutoPilot,
    updateAutoPilotSuccess,
    updateAutoPilotFailure,

    deleteAutoPilot,
    deleteAutoPilotSuccess,
    deleteAutoPilotFailure,
};
