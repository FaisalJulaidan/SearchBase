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
    logout,
    refreshToken,
    checkAuthTimeout
};