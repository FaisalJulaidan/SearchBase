import * as actionTypes from './actionTypes';


const getOptions = () => ({
    type: actionTypes.FETCH_OPTIONS_REQUEST,
});

const getOptionsSuccess = (options) => ({
    type: actionTypes.FETCH_OPTIONS_SUCCESS,
    options
});


const getOptionsFailure = (error) => ({
    type: actionTypes.FETCH_OPTIONS_FAILURE,
    error
});


export const optionsActions = {
    getOptions,
    getOptionsSuccess,
    getOptionsFailure,
};
