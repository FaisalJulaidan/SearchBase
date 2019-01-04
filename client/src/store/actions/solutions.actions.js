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

const addSolution = (params) => {
    console.log(params);
    return {
        type: actionTypes.ADD_SOLUTION_REQUEST,
        params
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

const editSolution = (params) => {
    return {
        type: actionTypes.EDIT_SOLUTION_REQUEST,
        params
    }
};

const editSolutionSuccess = (message) => {
    return {
        type: actionTypes.EDIT_SOLUTION_SUCCESS,
        message
    }
};

const editSolutionFailure = (error) => {
    return {
        type: actionTypes.EDIT_SOLUTION_FAILURE,
        error
    }
};

const updateSolutionInformationToDisplay = (params) => {
    return {
        type: actionTypes.UPDATE_SOLUTION_INFORMATION_TO_DISPLAY_REQUEST,
        params
    }
};

const updateSolutionInformationToDisplaySuccess = (params) => {
    return {
        type: actionTypes.UPDATE_SOLUTION_INFORMATION_TO_DISPLAY_SUCCESS,
        params
    }
};

const updateSolutionInformationToDisplayFailure = (params) => {
    return {
        type: actionTypes.UPDATE_SOLUTION_INFORMATION_TO_DISPLAY_FAILURE,
        params
    }
};

const updateButtonLink = (params) => {
    return {
        type: actionTypes.UPDATE_BUTTON_LINK_REQUEST,
        params
    }
};

const updateButtonLinkSuccess = (params) => {
    return {
        type: actionTypes.UPDATE_BUTTON_LINK_SUCCESS,
        params
    }
};

const updateButtonLinkFailure = (params) => {
    return {
        type: actionTypes.UPDATE_BUTTON_LINK_FAILURE,
        params
    }
};

const sendSolutionAlert = (params) => {
    return {
        type: actionTypes.SEND_SOLUTION_ALERT_REQUEST,
        params
    }
};

const sendSolutionAlertSuccess = (params) => {
    return {
        type: actionTypes.SEND_SOLUTION_ALERT_SUCCESS,
        params
    }
};

const sendSolutionAlertFailure = (params) => {
    return {
        type: actionTypes.SEND_SOLUTION_ALERT_FAILURE,
        params
    }
};

const updateAutomaticSolutions = (params) => {
    return {
        type: actionTypes.UPDATE_AUTOMATIC_SOLUTION_ALERTS_REQUEST,
        params
    }
};

const updateAutomaticSolutionsSuccess = (params) => {
    return {
        type: actionTypes.UPDATE_AUTOMATIC_SOLUTION_ALERTS_SUCCESS,
        params
    }
};

const updateAutomaticSolutionsFailure = (params) => {
    return {
        type: actionTypes.UPDATE_AUTOMATIC_SOLUTION_ALERTS_FAILURE,
        params
    }
};

export const solutionsActions = {
    getSolutions,
    getSolutionsSuccess,
    getSolutionsFailure,
    addSolution,
    addSolutionSuccess,
    addSolutionFailure,
    editSolution,
    editSolutionSuccess,
    editSolutionFailure,
    updateSolutionInformationToDisplay,
    updateSolutionInformationToDisplaySuccess,
    updateSolutionInformationToDisplayFailure,
    updateButtonLink,
    updateButtonLinkSuccess,
    updateButtonLinkFailure,
    sendSolutionAlert,
    sendSolutionAlertSuccess,
    sendSolutionAlertFailure,
    updateAutomaticSolutions,
    updateAutomaticSolutionsSuccess,
    updateAutomaticSolutionsFailure
};