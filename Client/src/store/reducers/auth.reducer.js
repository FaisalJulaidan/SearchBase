import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

let user = JSON.parse(localStorage.getItem('user'));
const initialState = user ?
    {
        isAuthenticated: true,
        user,
        isRequestingDemo: false,
        isSigningUp: false,
        isLoggingIn: false,
        errorMsg: null
    }
    :
    {
        isAuthenticated: false,
        user: null,
        companyID: null,
        isRequestingDemo: false,
        isSigningUp: false,
        isLoggingIn: false,
        errorMsg: null
    };

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
                user: action.user,
                role: action.role
            });
        case actionTypes.LOGIN_FAILURE:
            return updateObject(state, {
                isLoggingIn: false,
                isAuthenticated: false,
                user: null,
                role: null,
                errorMsg: action.error
            });


        case actionTypes.SIGNUP_REQUEST:
            return updateObject(state, {
                companyID: null,
                isSigningUp: true,
                errorMsg: null,
            });
        case actionTypes.SIGNUP_SUCCESS:
            return updateObject(state, {
                companyID: action.companyID,
                isSigningUp: false,
                errorMsg: null
            });
        case actionTypes.SIGNUP_FAILURE:
            return updateObject(state, {
                companyID: null,
                isSigningUp: false,
                errorMsg: action.error
            });

        case actionTypes.DEMO_REQUEST:
            return updateObject(state, {
                isRequestingDemo: true,
                errorMsg: null,
            });
        case actionTypes.DEMO_SUCCESS:
            return updateObject(state, {
                isRequestingDemo: false,
            });
        case actionTypes.DEMO_FAILURE:
            return updateObject(state, {
                isRequestingDemo: false,
                errorMsg: action.error
            });


        case actionTypes.RESET_PASSWORD_REQUEST:
            return updateObject(state, {});
        case actionTypes.RESET_PASSWORD_SUCCESS:
            return updateObject(state, {});
        case actionTypes.RESET_PASSWORD_FAILURE:
            return updateObject(state, {
                errorMsg: action.error
            });


        case actionTypes.NEW_RESET_PASSWORD_REQUEST:
            return updateObject(state, {});
        case actionTypes.NEW_RESET_PASSWORD_SUCCESS:
            return updateObject(state, {});
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

        case actionTypes.VERIFY_ACCOUNT_REQUEST:
            return updateObject(state, {
                errorMsg: null,
            });
        case actionTypes.VERIFY_ACCOUNT_SUCCESS:
            return updateObject(state, {});
        case actionTypes.VERIFY_ACCOUNT_FAILURE:
            return updateObject(state, {
                errorMsg: action.error
            });

        default:
            return state
    }
};
