import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

let user = JSON.parse(localStorage.getItem('user'));
const initialState = user ? {isAuthenticated: true, user,  isSigningUp: false, isLoggingIn: false, errorMsg: null} :
    {isAuthenticated: false, user: null,  isSigningUp: false, isLoggingIn: false, errorMsg: null};

export const auth = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.LOGIN_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isLoggingIn: true,
            });
        case actionTypes.LOGIN_SUCCESS:
            return updateObject(state, {
                isLoggingIn: false,
                isAuthenticated: true,
                user: action.user
            });
        case actionTypes.LOGIN_FAILURE:
            return updateObject(state, {
                isLoggingIn: false,
                isAuthenticated: false,
                user: null,
                errorMsg: action.error
            });


        case actionTypes.SIGNUP_REQUEST:
            return updateObject(state, {
                isSigningUp: true,
                errorMsg: null,
            });
        case actionTypes.SIGNUP_SUCCESS:
            return updateObject(state, {
                isSigningUp: false,
            });
        case actionTypes.SIGNUP_FAILURE:
            return updateObject(state, {
                isSigningUp: false,
                errorMsg: action.error
            });


        case actionTypes.RESET_PASSWORD_REQUEST:
            return updateObject(state, {
            });
        case actionTypes.RESET_PASSWORD_SUCCESS:
            return updateObject(state, {
            });
        case actionTypes.RESET_PASSWORD_FAILURE:
            return updateObject(state, {
                errorMsg: action.error
            });


        case actionTypes.NEW_RESET_PASSWORD_REQUEST:
            return updateObject(state, {
            });
        case actionTypes.NEW_RESET_PASSWORD_SUCCESS:
            return updateObject(state, {
            });
        case actionTypes.NEW_RESET_PASSWORD_FAILURE:
            return updateObject(state, {
                errorMsg: action.error
            });

        case actionTypes.LOGOUT:
            return updateObject(state, {
                isLoggingIn: false,
                isAuthenticated: false,
                user: null,
                errorMsg: null
            });
        default:
            return state
    }
};