import * as actionTypes from './actionTypes';

const getSolutions = (assistantID) => {
    return {
        type: actionTypes.GET_SOLUTIONS_REQUEST,
        assistantID
    }
};

const getSolutionsSuccess = (solutions) => {
    return {
        type: actionTypes.GET_SOLUTIONS_SUCCESS,
        solutionsData: solutions.data
    }
};

const getSolutionsFailure = (error) => {
    return {
        type: actionTypes.GET_SOLUTIONS_FAILURE,
        error
    }
};

export const solutionsActions = {
    getSolutions,
    getSolutionsSuccess,
    getSolutionsFailure
};