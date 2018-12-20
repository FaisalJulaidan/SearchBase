import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {isLoading: false, errorMsg: null};

export const profile = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.GET_PROFILE_REQUEST:
            return updateObject(state, {
                profile: {},
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.GET_PROFILE_SUCCESS:
            return updateObject(state, {
                successMsg: action.profile,
                isLoading: false
            });
        case actionTypes.GET_PROFILE_FAILURE:
            return updateObject(state, {
                profile: {},
                isLoading: false,
                errorMsg: action.error.msg
            });
        case actionTypes.SAVE_PROFILE_DETAILS_REQUEST:
            return updateObject(state, {
                successMsg: null,
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.SAVE_PROFILE_DETAILS_SUCCESS:
            return updateObject(state, {
                successMsg: action.successMsg,
                isLoading: false
            });
        case actionTypes.SAVE_PROFILE_DETAILS_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error.msg
            });
        case actionTypes.SAVE_DATA_SETTINGS_REQUEST:
            return updateObject(state, {
                successMsg: null,
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.SAVE_DATA_SETTINGS_SUCCESS:
            return updateObject(state, {
                successMsg: action.successMsg,
                isLoading: false
            });
        case actionTypes.SAVE_DATA_SETTINGS_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error.msg
            });
        default:
            return state
    }
};