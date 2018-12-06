import * as actionTypes from './actionTypes';


const updateSettingsRequest = (args) => {
    return {
        type: actionTypes.UPDATE_SETTINGS_REQUEST,
        ...args
    };
};

const updateSettingsSuccess = (successMsg) => {
    return {
        type: actionTypes.UPDATE_SETTINGS_SUCCESS,
        successMsg
    };
};

const updateSettingsFailure = (error) => {
    return {
        type: actionTypes.UPDATE_SETTINGS_FAILURE,
        error
    };
};

export const settingsActions = {
    updateSettingsRequest,
    updateSettingsSuccess,
    updateSettingsFailure
};