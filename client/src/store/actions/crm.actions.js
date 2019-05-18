import * as actionTypes from './actionTypes';

const getConnectedCRMs = () => {
    return {
        type: actionTypes.GET_CONNECTED_CRMS_REQUEST,
    };
};

const getConnectedCRMsSuccess = (CRMsList, msg) => {
    return {
        type: actionTypes.GET_CONNECTED_CRMS_SUCCESS,
        CRMsList,
        msg
    };
};

const getConnectedCRMsFailure = (error) => {
    return {
        type: actionTypes.GET_CONNECTED_CRMS_FAILURE,
        error
    };
};

const connectCrm = (connectedCRM) => {
    return {
        type: actionTypes.CONNECT_CRM_REQUEST,
        connectedCRM
    };
};

const connectCrmSuccess = (connectedCRM_ID, msg) => {
    return {
        type: actionTypes.CONNECT_CRM_SUCCESS,
        connectedCRM_ID,
        msg
    };
};

const connectCrmFailure = (error) => {
    return {
        type: actionTypes.CONNECT_CRM_FAILURE,
        error
    };
};

const testCrm = (testedCRM) => {
    return {
        type: actionTypes.TEST_CRM_REQUEST,
        testedCRM
    };
};

const testCrmSuccess = () => {
    return {
        type: actionTypes.TEST_CRM_SUCCESS,
    };
};

const testCrmFailure = (error) => {
    return {
        type: actionTypes.TEST_CRM_FAILURE,
        error
    };
};

const disconnectCrm = (disconnectedCRM) => {
    return {
        type: actionTypes.DISCONNECT_CRM_REQUEST,
        disconnectedCRM
    };
};

const disconnectCrmSuccess = (connectedCRM_ID, msg) => {
    return {
        type: actionTypes.DISCONNECT_CRM_SUCCESS,
        connectedCRM_ID,
        msg
    };
};

const disconnectCrmFailure = (error) => {
    return {
        type: actionTypes.DISCONNECT_CRM_FAILURE,
        error
    };
};


export const crmActions = {
    getConnectedCRMs,
    getConnectedCRMsSuccess,
    getConnectedCRMsFailure,

    connectCrm,
    connectCrmSuccess,
    connectCrmFailure,

    testCrm,
    testCrmSuccess,
    testCrmFailure,

    disconnectCrm,
    disconnectCrmSuccess,
    disconnectCrmFailure,


};
