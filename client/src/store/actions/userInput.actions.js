import * as actionTypes from './actionTypes';


const fetchUserInputs = (assistantID) => {
    return {
        type: actionTypes.FETCH_USERINPUT_REQUEST,
        assistantID
    };
};

const fetchUserInputsSuccess = (userInputs) => {
    return {
        type: actionTypes.FETCH_USERINPUT_SUCCESS,
        userInputs
    };
};

const fetchUserInputsFailure = (error) => {
    return {
        type: actionTypes.FETCH_USERINPUT_FAILURE,
        error
    };
};


const clearAllUserInputs = (assistantID) => {
    return {
        type: actionTypes.CLEAR_ALL_USERINPUT_REQUEST,
        assistantID
    };
};

const clearAllUserInputsSuccess = () => {
    return {
        type: actionTypes.CLEAR_ALL_USERINPUT_SUCCESS,
    };
};

const clearAllUserInputsFailure = (error) => {
    return {
        type: actionTypes.CLEAR_ALL_USERINPUT_FAILURE,
        error
    };
};


export const userInputActions = {
    fetchUserInputs,
    fetchUserInputsSuccess,
    fetchUserInputsFailure,

    clearAllUserInputs,
    clearAllUserInputsSuccess,
    clearAllUserInputsFailure
};