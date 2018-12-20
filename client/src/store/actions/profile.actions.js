import * as actionTypes from './actionTypes';

const getProfile = () => {
    return {
        type: actionTypes.GET_PROFILE_REQUEST
    }
};

const getProfileSuccess = (profileData) => {
    return {
        type: actionTypes.GET_PROFILE_SUCCESS,
        profileData
    }
};

const getProfileFailure = (error) => {
    return {
        type: actionTypes.GET_PROFILE_FAILURE,
        error
    }
};

const saveProfile = (profileData) => {
    return {
        type: actionTypes.GET_PROFILE_REQUEST,
        profileData
    }
};

const getProfileSuccess = (profileData) => {
    return {
        type: actionTypes.GET_PROFILE_SUCCESS,
        profileData
    }
};

const getProfileFailure = (error) => {
    return {
        type: actionTypes.GET_PROFILE_FAILURE,
        error
    }
};