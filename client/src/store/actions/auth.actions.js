import * as actionTypes from './actionTypes';


function login(email, password, prevPath) {
    return {
        type: actionTypes.LOGIN_REQUEST,
        email,
        password,
        prevPath
    };
}

function loginSuccess (user, role) {
    return {
        type: actionTypes.LOGIN_SUCCESS,
        user,
        role
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


function newResetPassword (data) {
    return {
        type: actionTypes.NEW_RESET_PASSWORD_REQUEST,
        data
    };
}

function newResetPasswordSuccess () {
    return {
        type: actionTypes.NEW_RESET_PASSWORD_SUCCESS,
    };
}

function newResetPasswordFailure (error) {
    return {
        type: actionTypes.NEW_RESET_PASSWORD_FAILURE,
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

    signup,
    signupSuccess,
    signupFailure,

    resetPassword,
    resetPasswordSuccess,
    resetPasswordFailure,

    newResetPassword,
    newResetPasswordSuccess,
    newResetPasswordFailure,

    logout,
};
