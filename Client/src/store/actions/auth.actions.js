import * as actionTypes from './actionTypes';


const login = (email, password, prevPath) => ({
    type: actionTypes.LOGIN_REQUEST,
    email,
    password,
    prevPath
});

const loginSuccess = (user, role) => ({
    type: actionTypes.LOGIN_SUCCESS,
    user,
    role
});

const loginFailure = (error) => ({
    type: actionTypes.LOGIN_FAILURE,
    error
});

const signup = (signupDetails) => ({
    type: actionTypes.SIGNUP_REQUEST,
    signupDetails
});

const signupSuccess = () => ({
    type: actionTypes.SIGNUP_SUCCESS,
});

const signupFailure = (error) => ({
    type: actionTypes.SIGNUP_FAILURE,
    error
});


const resetPassword = (data) => ({
    type: actionTypes.RESET_PASSWORD_REQUEST,
    data
});

const resetPasswordSuccess = () => ({
    type: actionTypes.RESET_PASSWORD_SUCCESS,
});

const resetPasswordFailure = (error) => ({
    type: actionTypes.RESET_PASSWORD_FAILURE,
    error
});


const newResetPassword = (data) => ({
    type: actionTypes.NEW_RESET_PASSWORD_REQUEST,
    data
});

const newResetPasswordSuccess = () => ({
    type: actionTypes.NEW_RESET_PASSWORD_SUCCESS,
});

const newResetPasswordFailure = (error) => ({
    type: actionTypes.NEW_RESET_PASSWORD_FAILURE,
    error
});


const logout = () => ({
    type: actionTypes.LOGOUT
});

const verifyAccount = (token) => ({
    type: actionTypes.VERIFY_ACCOUNT_REQUEST,
    meta: {thunk: true},
    token
});

const verifyAccountSuccess = (msg) => ({
    type: actionTypes.VERIFY_ACCOUNT_SUCCESS,
    msg
});

const verifyAccountFailure = (error) => ({
    type: actionTypes.VERIFY_ACCOUNT_FAILURE,
    error
});


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

    verifyAccount,
    verifyAccountSuccess,
    verifyAccountFailure,
};
