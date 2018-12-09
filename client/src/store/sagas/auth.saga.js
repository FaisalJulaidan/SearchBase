import * as actionTypes from '../actions/actionTypes';
import {put, takeEvery, all} from 'redux-saga/effects'
import {authActions} from "../actions";
import {history} from '../../helpers'
import axios from 'axios';
 

function* login(action) {
    const {email, password} = action;

    try {
        const res = yield axios.post(`/api/auth`, {email, password}, {
            headers: {'Content-Type': 'application/json'},
        });
        const user = res.data.data.user;
        // const expirationDate = yield new Date(
        //     new Date().getTime() + response.data.expiresIn * 1000
        // );

        yield localStorage.setItem("user", JSON.stringify(user));
        yield put(authActions.loginSuccess(user));
        // yield put(actions.checkAuthTimeout(response.data.expiresIn));

        yield history.push('/dashboard');
    } catch (error) {
        console.log(error)
        yield put(authActions.loginFailure(error.response.data));
    }
}

function* watchLogin() {
    yield takeEvery(actionTypes.LOGIN_REQUEST, login)
}

function* logout() {
    // remove user from local storage to log user out
    yield localStorage.removeItem('user');
    yield history.push('/login');
}

function* watchLogout() {
    yield takeEvery(actionTypes.LOGOUT, logout)
}

export function* authSaga() {
    yield all([
        watchLogin(),
        watchLogout()
    ])
}
