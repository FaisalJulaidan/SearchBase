import * as actionTypes from '../actions/actionTypes';
import { delay } from "redux-saga";
import { put, takeEvery, takeLatest, all } from 'redux-saga/effects'
import { authActions } from "../actions";
import { history, checkAuthenticity } from '../../helpers'
import {alertError, alertSuccess, destroyMessage, loadingMessage} from "../../helpers/alert";
import axios from 'axios';


function* checkAuthTimeout({expirationTime, refresh}) {
    yield delay(expirationTime * 1000);
    yield put(authActions.refreshToken(refresh));
}

function* watchCheckAuthTimeout() {
    yield takeEvery(actionTypes.AUTH_CHECK_TIMEOUT, checkAuthTimeout)
}

function* login({email, password}) {
    try {
        loadingMessage('Logging you in...');
        const res = yield axios.post(`/api/auth`, {email, password}, {
            headers: {'Content-Type': 'application/json'},
        });
        console.log("RES:", res);
        const {user, token, refresh, expiresIn} = yield res.data.data;
        yield localStorage.setItem("user", JSON.stringify(user));
        yield localStorage.setItem("token", token);
        yield localStorage.setItem("refresh", refresh);
        yield localStorage.setItem("expiresIn", expiresIn);
        // When access token expires in seconds
        const secondsToExpire = yield (new Date(expiresIn).getTime() - new Date().getTime()) / 1000;
        // Dispatch actions
        yield destroyMessage();
        yield put(authActions.loginSuccess(user));
        yield put(authActions.checkAuthTimeout(secondsToExpire, refresh)); // refresh to access token when expired
        // Redirect to dashboard page
        yield history.push('/dashboard');
    } catch (error) {
        console.log(error);
        yield destroyMessage();
        yield alertError('Log in Unsuccessful', error.response.data.msg);
        yield put(authActions.loginFailure(error.response.data));
    }
}

function* watchLogin() {
    yield takeLatest(actionTypes.LOGIN_REQUEST, login)
}

function* logout() {
    // Clear local storage from user, token...
    yield localStorage.clear();
    yield history.push('/login');
}

function* watchLogout() {
    yield takeLatest(actionTypes.LOGOUT, logout)
}

function* refreshToken({refresh}) {
    try {
        if(!checkAuthenticity()){throw new Error('Authentication Failed')}
        const res = yield axios.post(`/api/auth/refresh`, null,{
            headers: {'Authorization': 'Bearer ' + refresh},
        });

        const {token, expiresIn} = res.data.data;
        yield localStorage.setItem("token", token);
        yield localStorage.setItem("expiresIn", expiresIn);
        const secondsToExpire = yield (new Date(expiresIn).getTime() - new Date().getTime()) / 1000;
        yield put(authActions.checkAuthTimeout(secondsToExpire, refresh));


    } catch (error) {
        console.log(error);
        // Log the user out
        yield put(authActions.logout());
    }
}

function* watchRefreshToken() {
    yield takeEvery(actionTypes.REFRESH_TOKEN, refreshToken)
}

export function* authSaga() {
    yield all([
        watchLogin(),
        watchLogout(),
        watchCheckAuthTimeout(),
        watchRefreshToken()
    ])
}
