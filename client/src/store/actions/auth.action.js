import * as actionTypes from './actionTypes';


export function login (email, password) {
    return {
        type: actionTypes.LOGIN_REQUEST,
        email,
        password
    };
}

export function loginSuccess (user) {
    return {
        type: actionTypes.LOGIN_SUCCESS,
        user
    };
}

export function loginFailure (error) {
    return {
        type: actionTypes.LOGIN_FAILURE,
        error
    };
}


const logout = () => {
    return {
        type: actionTypes.LOGOUT
    };
};

export const authActions = {
    login,
    loginSuccess,
    loginFailure,
    logout
};