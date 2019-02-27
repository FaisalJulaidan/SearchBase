import * as actionTypes from './actionTypes';

const getProfile = () => {
    return {
        type: actionTypes.GET_PROFILE_REQUEST
    }
};

const getProfileSuccess = (profile) => {
    return {
        type: actionTypes.GET_PROFILE_SUCCESS,
        profileData: profile
    }
};

const getProfileFailure = (error) => {
    return {
        type: actionTypes.GET_PROFILE_FAILURE,
        error
    }
};

const saveProfileDetails = (profileData) => {
    return {
        type: actionTypes.SAVE_PROFILE_DETAILS_REQUEST,
        profileData
    }
};

const saveProfileDetailsSuccess = (successMsg) => {
    return {
        type: actionTypes.SAVE_PROFILE_DETAILS_SUCCESS,
        successMsg
    }
};

const saveProfileDetailsFailure = (error) => {
    return {
        type: actionTypes.SAVE_PROFILE_DETAILS_FAILURE,
        error
    }
};

const saveDataSettings = (dataSettings) => {
    return {
        type: actionTypes.SAVE_DATA_SETTINGS_REQUEST,
        dataSettings
    }
};

const saveDataSettingsSuccess = (successMsg) => {
    return {
        type: actionTypes.SAVE_DATA_SETTINGS_SUCCESS,
        successMsg
    }
};

const saveDataSettingsFailure = (error) => {
    return {
        type: actionTypes.SAVE_DATA_SETTINGS_FAILURE,
        error
    }
};


const changePassword = (oldPassword, newPassword) => {
    return {
        type: actionTypes.CHANGE_PASS_REQUEST,
        oldPassword,
        newPassword
    }
};

const changePasswordSuccess = (successMsg) => {
    return {
        type: actionTypes.CHANGE_PASS_SUCCESS,
        successMsg
    }
};

const changePasswordFailure = (error) => {
    return {
        type: actionTypes.CHANGE_PASS_FAILURE,
        error
    }
};

export const profileActions = {
    getProfile,
    getProfileSuccess,
    getProfileFailure,
    saveProfileDetails,
    saveProfileDetailsSuccess,
    saveProfileDetailsFailure,
    saveDataSettings,
    saveDataSettingsSuccess,
    saveDataSettingsFailure,

    changePassword,
    changePasswordSuccess,
    changePasswordFailure,
};