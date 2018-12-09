import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

let user = JSON.parse(localStorage.getItem('user'));
const initialState = user ? {isAuthenticated: true, user, isLoggingIn: false, errorMsg: ''} :
    {isAuthenticated: false, user: null, isLoggingIn: false, errorMsg: ''};

export const auth = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.LOGIN_REQUEST:
            return updateObject(state, {
                errorMsg: '',
                isLoggingIn: true,
            });
        case actionTypes.LOGIN_SUCCESS:
            return updateObject(state, {
                isLoggingIn: false,
                isAuthenticated: true,
                user: action.user,
            });
        case actionTypes.LOGIN_FAILURE:
            return updateObject(state, {
                isLoggingIn: false,
                isAuthenticated: false,
                user: null,
                errorMsg: action.error.msg
            });
        case actionTypes.LOGOUT:
            return updateObject(state, {
                isLoggingIn: false,
                isAuthenticated: false,
                user: null,
                errorMsg: ''
            });
        default:
            return state
    }
};