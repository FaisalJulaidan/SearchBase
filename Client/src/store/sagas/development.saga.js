import * as actionTypes from '../actions/actionTypes';
import {all, put, takeLatest} from 'redux-saga/effects'
import {developmentActions} from "../actions";
import {errorMessage, http, loadingMessage, successMessage} from "helpers";


function* getWebhookList() {
    try {
        const res = yield http.get(`/webhooks`);
        const available = yield http.get(`/webhooks/available`);
        yield put(developmentActions.fetchDevSuccess(res.data.data, available.data.data));
    } catch (error) {
        console.log(error)
        const msg = error.response?.data?.msg || "Couldn't load webhook list";
        yield put(developmentActions.fetchDevFailure(msg));
        errorMessage(msg);

    }
}

function* saveWebhook({ID, newSettings}) {
    try {
        console.log(ID)
        const res = yield http.put(`/webhook`, {id: ID, ...newSettings});
        yield put(developmentActions.saveWebhookSuccess(ID));
        successMessage("Succesfully saved webhook")
    } catch (error) {
        console.log(error)
        const msg = error.response?.data?.msg || "Couldn't save webhook";
        yield put(developmentActions.saveWebhookFailure(msg, ID));
        errorMessage(msg);
    }
}

function* watchGetWebhookList() {
    yield takeLatest(actionTypes.FETCH_DEV_REQUEST, getWebhookList)
}


function* watchSaveWebhook() {
    yield takeLatest(actionTypes.SAVE_WEBHOOK_REQUEST, saveWebhook)
}


export function* developmentSaga() {
    yield all([
        watchGetWebhookList(),
        watchSaveWebhook()
    ])
}
