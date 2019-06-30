import * as actionTypes from '../actions/actionTypes';
import {all, put, takeLatest} from 'redux-saga/effects'
import {authActions} from "../actions";
import {history, successMessage} from "helpers";
import {errorMessage, loadingMessage, warningMessage} from "helpers/alert";
import axios from 'axios';


// Login
function* login({email, password, prevPath}) {
    try {
        loadingMessage('Logging you in...');
        const res = yield axios.post(`/api/auth`, {email, password}, {
            headers: {'Content-Type': 'application/json'},
        });

        const {user, role, token, refresh, expiresIn} = yield res.data.data;
        yield localStorage.setItem("user", JSON.stringify(user));
        yield localStorage.setItem("role", JSON.stringify(role));
        yield localStorage.setItem("token", token);
        yield localStorage.setItem("refresh", refresh);
        yield localStorage.setItem("expiresIn", expiresIn);

        // Dispatch actions
        // yield put(profileActions.getProfile());
        yield put(authActions.loginSuccess(user, role));

        // Redirect to dashboard page
        yield history.push(prevPath || '/dashboard');

    } catch (error) {
        const msg = error.response?.data?.msg || 'Couldn\'t Login';
        yield put(authActions.loginFailure(error.response.data));
        errorMessage(msg, 0);
    }
}

// Signup
function* signup({signupDetails}) {
    try {
        loadingMessage('Creating your account', 0);
        const res = yield axios.post(`/api/signup`, {...signupDetails}, {
            headers: {'Content-Type': 'application/json'},
        });
        yield put(authActions.signupSuccess());
        successMessage('Account created');


        // Redirect to login ans ask user to verify account
        yield history.push('/login');
        warningMessage('Please check your email to verify your account', 0);

    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't signup";
        yield put(authActions.signupFailure(error.response.data));
        errorMessage(msg, 0);
    }
}

// Reset Password
function* forgetPassword({data}) {
    try {
        loadingMessage('Sending reset password email...', 0);
        yield axios.post(`/api/reset_password`, {...data}, {
            headers: {'Content-Type': 'application/json'},
        });
        yield put(authActions.resetPasswordSuccess());
        successMessage('Email to reset your password has been sent');
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't send reset password to this email";
        yield put(authActions.resetPasswordFailure(msg));
        errorMessage(msg, 0);

    }
}


function* newResetPassword({data}) {
    try {
        loadingMessage('Saving new password...', 0);
        yield axios.post(`/api/reset_password/` + data["payload"], {...data}, {
            headers: {'Content-Type': 'application/json'},
        });
        yield put(authActions.newResetPasswordSuccess());
        successMessage('The password for your account has been updated');

        yield history.push('/login');
        successMessage('Login using your new password', 0);

    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't update account password";
        yield put(authActions.newResetPasswordFailure(msg));
        errorMessage(msg, 0);
    }
}

// Logout
function* logout() {
    // Clear local storage from user, token...
    yield localStorage.clear();
    yield history.push('/login');
    successMessage('You have been logged out');
}


function* verifyAccount({token, meta}) {
    try {
        const res = yield axios.post(`/api/verify_account/${token}`, {}, {
            headers: {'Content-Type': 'application/json'},
        });
        successMessage(res.data?.msg || 'Account verified');
        yield put({...authActions.verifyAccountSuccess(res.data?.data), meta});
    } catch (error) {
        const msg = error.response?.data?.msg || 'Account validation is failed';
        errorMessage(msg);
        yield put({...authActions.verifyAccountFailure(msg), meta});
    }
}

function* watchVerifyAccount() {
    yield takeLatest(actionTypes.VERIFY_ACCOUNT_REQUEST, verifyAccount)
}


function* watchLogin() {
    yield takeLatest(actionTypes.LOGIN_REQUEST, login)
}

function* watchSignup() {
    yield takeLatest(actionTypes.SIGNUP_REQUEST, signup)
}

function* watchForgetPassword() {
    yield takeLatest(actionTypes.RESET_PASSWORD_REQUEST, forgetPassword)
}

function* watchNewResetPassword() {
    yield takeLatest(actionTypes.NEW_RESET_PASSWORD_REQUEST, newResetPassword)
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
        watchNewResetPassword(),
        watchVerifyAccount()

    ])
}