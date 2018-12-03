import {http} from '../../helpers';
import * as actionTypes from '../actions/actionTypes';
import {put, takeEvery, all} from 'redux-saga/effects'
import {authActions} from "../actions";

function* login(action) {
    const {email, password} = action;

    try {
        const res = yield http.post(`/api/auth`, {email, password});
        const user = res.data.data.user;
        // const expirationDate = yield new Date(
        //     new Date().getTime() + response.data.expiresIn * 1000
        // );

        yield localStorage.setItem("user", JSON.stringify(user));
        yield put(authActions.loginSuccess(user));
        // yield put(actions.checkAuthTimeout(response.data.expiresIn));
    } catch (error) {
        yield put(authActions.loginFailure(error.response.data));
    }
}

function* watchLogin() {
    yield takeEvery(actionTypes.LOGIN_REQUEST, login)
}

function* logout() {
    // remove user from local storage to log user out
    yield localStorage.removeItem('user');
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
