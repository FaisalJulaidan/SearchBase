import * as actionTypes from './actionTypes';

// Fetch All
const fetchAutoPilots = () => ({
    type: actionTypes.FETCH_AUTOPILOTS_REQUEST
});

const fetchAutoPilotsSuccess = (autoPilotsList) => ({
    type: actionTypes.FETCH_AUTOPILOTS_SUCCESS,
    autoPilotsList
});

const fetchAutoPilotsFailure = (errorMsg) => ({
    type: actionTypes.FETCH_AUTOPILOTS_FAILURE,
    errorMsg
});


// Fetch
const fetchAutoPilot = (autoPilotID) => ({
    type: actionTypes.FETCH_AUTOPILOT_REQUEST,
    meta: {thunk: true},
    autoPilotID
});

const fetchAutoPilotSuccess = (autoPilot) => ({
    type: actionTypes.FETCH_AUTOPILOT_SUCCESS,
    autoPilot
});

const fetchAutoPilotFailure = (errorMsg) => ({
    type: actionTypes.FETCH_AUTOPILOT_FAILURE,
    errorMsg
});


// Add
const addAutoPilot = (newAutoPilot) => ({
    type: actionTypes.ADD_AUTOPILOT_REQUEST,
    newAutoPilot
});

const addAutoPilotSuccess = (newAutoPilot, successMsg) => ({
    type: actionTypes.ADD_AUTOPILOT_SUCCESS,
    newAutoPilot,
    successMsg
});

const addAutoPilotFailure = (errorMsg) => ({
    type: actionTypes.ADD_AUTOPILOT_FAILURE,
    errorMsg
});


// Update
const updateAutoPilot = (autoPilotID, updatedValues) => ({
    type: actionTypes.UPDATE_AUTOPILOT_REQUEST,
    autoPilotID,
    updatedValues
});

const updateAutoPilotSuccess = (autoPilotID, updatedAutoPilot, successMsg) => ({
    type: actionTypes.UPDATE_AUTOPILOT_SUCCESS,
    autoPilotID,
    updatedAutoPilot,
    successMsg
});

const updateAutoPilotFailure = (errorMsg) => ({
    type: actionTypes.UPDATE_AUTOPILOT_FAILURE,
    errorMsg
});

// Update
const updateAutoPilotConfigs = (autoPilotID, updatedValues) => ({
    type: actionTypes.UPDATE_AUTOPILOT_CONFIGS_REQUEST,
    autoPilotID,
    updatedValues
});

const updateAutoPilotConfigsSuccess = (updatedAutoPilot, successMsg) => ({
    type: actionTypes.UPDATE_AUTOPILOT_CONFIGS_SUCCESS,
    updatedAutoPilot,
    successMsg
});

const updateAutoPilotConfigsFailure = (errorMsg) => ({
    type: actionTypes.UPDATE_AUTOPILOT_CONFIGS_FAILURE,
    errorMsg
});


// Delete
const deleteAutoPilot = (autoPilotID) => ({
    type: actionTypes.DELETE_AUTOPILOT_REQUEST,
    meta: {thunk: true},
    autoPilotID,
});

const deleteAutoPilotSuccess = (autoPilotID, successMsg) => ({
    type: actionTypes.DELETE_AUTOPILOT_SUCCESS,
    autoPilotID,
    successMsg
});

const deleteAutoPilotFailure = (errorMsg) => ({
    type: actionTypes.DELETE_AUTOPILOT_FAILURE,
    errorMsg
});


const updateStatus = (status, autoPilotID) => ({
    type: actionTypes.UPDATE_AUTOPILOT_STATUS_REQUEST,
    autoPilotID,
    status
});

const updateStatusSuccess = (successMsg, status, autoPilotID) => ({
    type: actionTypes.UPDATE_AUTOPILOT_STATUS_SUCCESS,
    successMsg,
    status,
    autoPilotID
});

const updateStatusFailure = (errorMsg) => ({
    type: actionTypes.UPDATE_AUTOPILOT_STATUS_FAILURE,
    errorMsg
});

export const autoPilotActions = {
    fetchAutoPilots,
    fetchAutoPilotsSuccess,
    fetchAutoPilotsFailure,

    fetchAutoPilot,
    fetchAutoPilotSuccess,
    fetchAutoPilotFailure,

    addAutoPilot,
    addAutoPilotSuccess,
    addAutoPilotFailure,

    updateAutoPilot,
    updateAutoPilotSuccess,
    updateAutoPilotFailure,

    updateAutoPilotConfigs,
    updateAutoPilotConfigsSuccess,
    updateAutoPilotConfigsFailure,

    deleteAutoPilot,
    deleteAutoPilotSuccess,
    deleteAutoPilotFailure,

    updateStatus,
    updateStatusSuccess,
    updateStatusFailure,
};
