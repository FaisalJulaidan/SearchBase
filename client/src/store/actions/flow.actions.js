import * as actionTypes from './actionTypes';


const fetchFlowRequest = (ID) => {
    return {
        type: actionTypes.FETCH_FLOW_REQUEST,
        ID
    };
};

const fetchFlowSuccess = (args) => {
    return {
        type: actionTypes.FETCH_FLOW_SUCCESS,
        ...args
    };
};

const fetchFlowFailure = (error) => {
    return {
        type: actionTypes.FETCH_FLOW_FAILURE,
        error
    };
};


export const flowActions = {
    fetchFlowRequest,
    fetchFlowSuccess,
    fetchFlowFailure
};