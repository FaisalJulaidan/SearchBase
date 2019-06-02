import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';
import {deepClone} from "../../helpers";

const initialState = {profile: {}, isLoading: false, errorMsg: null};

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
                profile: action.profileData,
                isLoading: false
            });
        case actionTypes.GET_PROFILE_FAILURE:
            return updateObject(state, {
                profile: {},
                isLoading: false,
                errorMsg: action.error
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
                errorMsg: action.error
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
                errorMsg: action.error
            });

        // Company Custom Logo
        case actionTypes.UPLOAD_LOGO_REQUEST:
            return updateObject(state, {
                errorMsg: null,
            });
        case actionTypes.UPLOAD_LOGO_SUCCESS:
            return updateObject(state, {
                successMsg: action.msg,
                profile: {...state.profile, company: {...state.profile.company, LogoPath: action.UpdatedLogoPath}}
            });
        case actionTypes.UPLOAD_LOGO_FAILURE:
            return updateObject(state, {
                errorMsg: action.error
            });

        case actionTypes.DELETE_LOGO_REQUEST:
            return updateObject(state, {
                errorMsg: null,
            });
        case actionTypes.DELETE_LOGO_SUCCESS:
            return updateObject(state, {
                successMsg: action.msg,
                profile: {...state.profile, company: {...state.profile.company, LogoPath: null}}
            });
        case actionTypes.DELETE_LOGO_FAILURE:
            return updateObject(state, {
                errorMsg: action.error
            });

        default:
            return state
    }
};