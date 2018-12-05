import * as actionTypes from './actionTypes';


const fetchFlowRequest = () => {
    return {
        type: actionTypes.FETCH_FLOW_REQUEST
    };
};

const fetchFlowSuccess = (assistantList) => {
    return {
        type: actionTypes.FETCH_FLOW_SUCCESS,
        assistantList
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