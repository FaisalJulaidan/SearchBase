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

const addSolution = (assistantID, solution) => {
    return {
        type: actionTypes.ADD_SOLUTION_REQUEST,
        assistantID,
        solution
    }
};

const addSolutionSuccess = (message) => {
    return {
        type: actionTypes.ADD_SOLUTION_SUCCESS,
        message
    }
};

const addSolutionFailure = (error) => {
    return {
        type: actionTypes.ADD_SOLUTION_FAILURE,
        error
    }
};

export const solutionsActions = {
    getSolutions,
    getSolutionsSuccess,
    getSolutionsFailure,
    addSolution,
    addSolutionSuccess,
    addSolutionFailure
};