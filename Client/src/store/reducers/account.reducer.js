import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {account: {}, isLoading: false, errorMsg: null};

export const account = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.GET_ACCOUNT_REQUEST:
            return updateObject(state, {
                account: {},
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.GET_ACCOUNT_SUCCESS:
            return updateObject(state, {
                account: action.account,
                isLoading: false
            });
        case actionTypes.GET_ACCOUNT_FAILURE:
            return updateObject(state, {
                account: {},
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


        case actionTypes.SAVE_COMPANY_DETAILS_REQUEST:
            return updateObject(state, {
                successMsg: null,
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.SAVE_COMPANY_DETAILS_SUCCESS:
            return updateObject(state, {
                successMsg: action.successMsg,
                isLoading: false
            });
        case actionTypes.SAVE_COMPANY_DETAILS_FAILURE:
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
            console.log(action)
            return updateObject(state, {
                successMsg: action.msg,
                account: {...state.account, company: {...state.account.company, LogoPath: action.UpdatedLogoPath, }}
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
                account: {...state.account, company: {...state.account.company, LogoPath: null}}
            });
        case actionTypes.DELETE_LOGO_FAILURE:
            return updateObject(state, {
                errorMsg: action.error
            });

        default:
            return state
    }
};