import * as actionTypes from './actionTypes';


function login (email, password) {
    return {
        type: actionTypes.LOGIN_REQUEST,
        email,
        password
    };
}

function loginSuccess (user) {
    return {
        type: actionTypes.LOGIN_SUCCESS,
        user
    };
}

function loginFailure (error) {
    return {
        type: actionTypes.LOGIN_FAILURE,
        error
    };
}

function signup (signupDetails) {
    return {
        type: actionTypes.SIGNUP_REQUEST,
        signupDetails
    };
}

function signupSuccess () {
    return {
        type: actionTypes.SIGNUP_SUCCESS,
    };
}

function signupFailure (error) {
    return {
        type: actionTypes.SIGNUP_FAILURE,
        error
    };
}


function resetPassword (data) {
    return {
        type: actionTypes.RESET_PASSWORD_REQUEST,
        data
    };
}

function resetPasswordSuccess () {
    return {
        type: actionTypes.RESET_PASSWORD_SUCCESS,
    };
}

function resetPasswordFailure (error) {
    return {
        type: actionTypes.RESET_PASSWORD_FAILURE,
        error
    };
}


const logout = () => {
    return {
        type: actionTypes.LOGOUT
    };
};

const checkAuthTimeout = (expirationTime, refresh) => {
    return {
        type: actionTypes.AUTH_CHECK_TIMEOUT,
        expirationTime, refresh
    };
};

const refreshToken = (refresh) => {
    return {
        type: actionTypes.REFRESH_TOKEN,
        refresh
    };
};

export const authActions = {
    login,
    loginSuccess,
    loginFailure,

    signup,
    signupSuccess,
    signupFailure,

    resetPassword,
    resetPasswordSuccess,
    resetPasswordFailure,

    logout,
    refreshToken,
    checkAuthTimeout
};