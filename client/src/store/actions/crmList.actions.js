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


export const crmListActions = {
    getConnectedCRMs,
    getConnectedCRMsSuccess,
    getConnectedCRMsFailure,
};
