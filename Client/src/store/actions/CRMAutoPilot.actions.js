import * as actionTypes from './actionTypes';

// Fetch All
const fetchCRMAutoPilots = () => ({
    type: actionTypes.FETCH_CRM_AUTOPILOTS_REQUEST
});

const fetchCRMAutoPilotsSuccess = (CRMAutoPilotsList) => ({
    type: actionTypes.FETCH_CRM_AUTOPILOTS_SUCCESS,
    CRMAutoPilotsList
});

const fetchCRMAutoPilotsFailure = (errorMsg) => ({
    type: actionTypes.FETCH_CRM_AUTOPILOTS_FAILURE,
    errorMsg
});


// Fetch
const fetchCRMAutoPilot = (CRMAutoPilotID) => ({
    type: actionTypes.FETCH_CRM_AUTOPILOT_REQUEST,
    meta: {thunk: true},
    CRMAutoPilotID
});

const fetchCRMAutoPilotSuccess = (CRMAutoPilot) => ({
    type: actionTypes.FETCH_CRM_AUTOPILOT_SUCCESS,
    CRMAutoPilot
});

const fetchCRMAutoPilotFailure = (errorMsg) => ({
    type: actionTypes.FETCH_CRM_AUTOPILOT_FAILURE,
    errorMsg
});




// Add
const addCRMAutoPilot = (newCRMAutoPilot) => ({
    type: actionTypes.ADD_CRM_AUTOPILOT_REQUEST,
    newCRMAutoPilot
});

const addCRMAutoPilotSuccess = (newCRMAutoPilot, successMsg) => ({
    type: actionTypes.ADD_CRM_AUTOPILOT_SUCCESS,
    newCRMAutoPilot,
    successMsg
});

const addCRMAutoPilotFailure = (errorMsg) => ({
    type: actionTypes.ADD_CRM_AUTOPILOT_FAILURE,
    errorMsg
});


// Update
const updateCRMAutoPilot = (CRMAutoPilotID, updatedValues) => ({
    type: actionTypes.UPDATE_CRM_AUTOPILOT_REQUEST,
    CRMAutoPilotID,
    updatedValues
});

const updateCRMAutoPilotSuccess = (CRMAutoPilotID, updatedCRMAutoPilot, successMsg) => ({
    type: actionTypes.UPDATE_CRM_AUTOPILOT_SUCCESS,
    CRMAutoPilotID,
    updatedCRMAutoPilot,
    successMsg
});

const updateCRMAutoPilotFailure = (errorMsg) => ({
    type: actionTypes.UPDATE_CRM_AUTOPILOT_FAILURE,
    errorMsg
});

// Update
const updateCRMAutoPilotConfigs = (CRMAutoPilotID, updatedValues) => ({
    type: actionTypes.UPDATE_CRM_AUTOPILOT_CONFIGS_REQUEST,
    CRMAutoPilotID,
    updatedValues
});

const updateCRMAutoPilotConfigsSuccess = (CRMUpdatedAutoPilot, successMsg) => ({
    type: actionTypes.UPDATE_CRM_AUTOPILOT_CONFIGS_SUCCESS,
    CRMUpdatedAutoPilot,
    successMsg
});

const updateCRMAutoPilotConfigsFailure = (errorMsg) => ({
    type: actionTypes.UPDATE_CRM_AUTOPILOT_CONFIGS_FAILURE,
    errorMsg
});


// Delete
const deleteCRMAutoPilot = (CRMAutoPilotID) => ({
    type: actionTypes.DELETE_CRM_AUTOPILOT_REQUEST,
    meta: {thunk: true},
    CRMAutoPilotID,
});

const deleteCRMAutoPilotSuccess = (CRMAutoPilotID, successMsg) => ({
    type: actionTypes.DELETE_CRM_AUTOPILOT_SUCCESS,
    CRMAutoPilotID,
    successMsg
});

const deleteCRMAutoPilotFailure = (errorMsg) => ({
    type: actionTypes.DELETE_CRM_AUTOPILOT_FAILURE,
    errorMsg
});


const updateStatus = ( CRMAutoPilotID, status) => ({
    type: actionTypes.UPDATE_CRM_AUTOPILOT_STATUS_REQUEST,
    CRMAutoPilotID,
    status
});

const updateStatusSuccess = (successMsg, status, CRMAutoPilotID) => ({
    type: actionTypes.UPDATE_CRM_AUTOPILOT_STATUS_SUCCESS,
    successMsg,
    status,
    CRMAutoPilotID
});

const updateStatusFailure = (errorMsg) => ({
    type: actionTypes.UPDATE_CRM_AUTOPILOT_STATUS_FAILURE,
    errorMsg
});

export const CRMAutoPilotActions = {
    fetchCRMAutoPilots,
    fetchCRMAutoPilotsSuccess,
    fetchCRMAutoPilotsFailure,

    fetchCRMAutoPilot,
    fetchCRMAutoPilotSuccess,
    fetchCRMAutoPilotFailure,

    addCRMAutoPilot,
    addCRMAutoPilotSuccess,
    addCRMAutoPilotFailure,

    updateCRMAutoPilot,
    updateCRMAutoPilotSuccess,
    updateCRMAutoPilotFailure,

    updateCRMAutoPilotConfigs,
    updateCRMAutoPilotConfigsSuccess,
    updateCRMAutoPilotConfigsFailure,

    deleteCRMAutoPilot,
    deleteCRMAutoPilotSuccess,
    deleteCRMAutoPilotFailure,

    updateStatus,
    updateStatusSuccess,
    updateStatusFailure,
};