import * as actionTypes from './actionTypes';


function getOptions () {
    return {
        type: actionTypes.FETCH_OPTIONS_REQUEST,
    };
}

function getOptionsSuccess (options) {
    return {
        type: actionTypes.FETCH_OPTIONS_SUCCESS,
        options
    };
}

function getOptionsFailure (error) {
    return {
        type: actionTypes.FETCH_OPTIONS_FAILURE,
        error
    };
}


export const optionsActions = {
    getOptions,
    getOptionsSuccess,
    getOptionsFailure,
};