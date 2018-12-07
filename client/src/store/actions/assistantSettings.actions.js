import * as actionTypes from './actionTypes';


const updateAssistantSettingsRequest = (args) => {
    return {
        type: actionTypes.UPDATE_ASSISTANT_SETTINGS_REQUEST,
        ...args
    };
};

const updateAssistantSettingsSuccess = (successMsg) => {
    return {
        type: actionTypes.UPDATE_ASSISTANT_SETTINGS_SUCCESS,
        successMsg
    };
};

const updateAssistantSettingsFailure = (error) => {
    return {
        type: actionTypes.UPDATE_ASSISTANT_SETTINGS_FAILURE,
        error
    };
};

export const assistantSettingsActions = {
    updateAssistantSettingsRequest,
    updateAssistantSettingsSuccess,
    updateAssistantSettingsFailure
};