import * as actionTypes from '../actions/actionTypes';
import { delay } from "redux-saga";
import { put, takeLatest, all } from 'redux-saga/effects'
import {authActions, profileActions} from "../actions";
import {history, checkAuthenticity, successMessage} from '../../helpers'
import {loadingMessage, errorMessage, warningMessage} from "../../helpers/alert";
import axios from 'axios';


// Login
function* login({email, password}) {
    try {
        loadingMessage('Logging you in...');
        const res = yield axios.post(`/api/auth`, {email, password}, {
            headers: {'Content-Type': 'application/json'},
        });

        const {user, token, refresh, expiresIn} = yield res.data.data;
        yield localStorage.setItem("user", JSON.stringify(user));
        yield localStorage.setItem("token", token);
        yield localStorage.setItem("refresh", refresh);
        yield localStorage.setItem("expiresIn", expiresIn);

        // Dispatch actions
        yield put(profileActions.getProfile());
        yield put(authActions.loginSuccess(user));

        // Redirect to dashboard page
        yield history.push('/dashboard');

    } catch (error) {
        console.log(error);
        yield put(authActions.loginFailure(error.response.data));
        yield errorMessage(error.response.data.msg, 0);


    }
}

function* watchLogin() {
    yield takeLatest(actionTypes.LOGIN_REQUEST, login)
}

// Signup
function* signup({signupDetails}) {

    try {
        loadingMessage('Creating your account', 0);
        const res = yield axios.post(`/api/signup`, {...signupDetails}, {
            headers: {'Content-Type': 'application/json'},
        });
        yield successMessage('Account created');
        yield put(authActions.signupSuccess());

        yield history.push('/login');
        yield warningMessage('Please verify your account', 0);

    } catch (error) {
        console.log(error);
        yield put(authActions.signupFailure(error.response.data));
        yield errorMessage(error.response.data.msg, 0);
    }
}

function* watchSignup() {
    yield takeLatest(actionTypes.SIGNUP_REQUEST, signup)
}


// Reset Password
function* forgetPassword({data}) {
    try {
        loadingMessage('Sending reset password email...', 0);
        yield axios.post(`/api/reset_password`, {...data}, {
            headers: {'Content-Type': 'application/json'},
        });
        yield successMessage('Email to reset your password has been sent');
        yield put(authActions.resetPasswordSuccess());

    } catch (error) {
        console.log(error);
        yield errorMessage('Could not send reset password email', 0);
        yield put(authActions.resetPasswordFailure(error.response.data));
    }
}

function* watchForgetPassword() {
    yield takeLatest(actionTypes.RESET_PASSWORD_REQUEST, forgetPassword)
}

function* newResetPassword({data}) {
    try {
        loadingMessage('Saving new password...', 0);
        yield axios.post(`/api/reset_password/`+data["payload"], {...data}, {
            headers: {'Content-Type': 'application/json'},
        });
        successMessage('The password for your account has been updated');
        yield put(authActions.newResetPasswordSuccess());
        yield history.push('/login');
        successMessage('Login using your new password', 0);

    } catch (error) {
        console.log(error);
        yield errorMessage('Could not update account password', 0);
        yield put(authActions.newResetPasswordFailure(error.response.data));
    }
}

function* watchNewResetPassword() {
    yield takeLatest(actionTypes.NEW_RESET_PASSWORD_REQUEST, newResetPassword)
}


// Logout
function* logout() {
    // Clear local storage from user, token...
    yield localStorage.clear();
    yield history.push('/login');
    yield successMessage('You have been logged out');

}

function* watchLogout() {
    yield takeLatest(actionTypes.LOGOUT, logout)
}


export function* authSaga() {
    yield all([
        watchLogin(),
        watchSignup(),
        watchForgetPassword(),
        watchLogout(),
        watchNewResetPassword()
    ])
}
