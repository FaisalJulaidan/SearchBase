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

export const authActions = {
    login,
    loginSuccess,
    loginFailure,
    logout
};