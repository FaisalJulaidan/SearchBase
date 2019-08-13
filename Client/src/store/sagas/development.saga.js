import * as actionTypes from '../actions/actionTypes';
import {all, put, takeLatest} from 'redux-saga/effects'
import {developmentActions} from "../actions";
import {errorMessage, http, loadingMessage, successMessage} from "helpers";


function* getWebhookList() {
    try {
        const res = yield http.get(`/webhooks`);
        yield put(developmentActions.fetchDevSuccess(res.data.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't load webhook list";
        yield put(developmentActions.fetchDevFailure(msg));
        errorMessage(msg);

    }
}
function* watchGetWebhookList() {
    yield takeLatest(actionTypes.FETCH_DEV_REQUEST, getWebhookList)
}

export function* developmentSaga() {
    yield all([
        watchGetWebhookList(),
    ])
}
