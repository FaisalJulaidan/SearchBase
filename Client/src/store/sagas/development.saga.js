import * as actionTypes from '../actions/actionTypes';
import { all, put, takeLatest } from 'redux-saga/effects';
import { developmentActions } from '../actions';
import { errorMessage, http, loadingMessage, successMessage } from 'helpers';


function* getWebhookList() {
    try {
        const res = yield http.get(`/webhooks`);
        yield put(developmentActions.fetchDevSuccess(res.data.data));
    } catch (error) {
        console.log(error);
        const msg = error.response?.data?.msg || 'Couldn\'t load webhook list';
        yield put(developmentActions.fetchDevFailure(msg));
        errorMessage(msg);

    }
}

function* createWebhook({ settings }) {
    try {
        loadingMessage('Creating webhook');
        const res = yield http.post(`/webhook`, settings);
        yield put(developmentActions.createWebhookSuccess(res.data.data));
        successMessage('Successfully created webhook');
    } catch (error) {
        console.log(error);
        const msg = error.response?.data?.msg || 'Couldn\'t create webhook';
        yield put(developmentActions.createWebhookFailure(msg));
        errorMessage(msg);
    }
}

function* saveWebhook({ ID, newSettings }) {
    try {
        console.log(ID);
        const res = yield http.put(`/webhook/${ID}`, newSettings);
        yield put(developmentActions.saveWebhookSuccess(ID));
        successMessage('Successfully saved webhook');
    } catch (error) {
        console.log(error);
        const msg = error.response?.data?.msg || 'Couldn\'t save webhook';
        yield put(developmentActions.saveWebhookFailure(msg, ID));
        errorMessage(msg);
    }
}

function* deleteWebhook({ ID }) {
    try {
        loadingMessage('Deleting webhook');
        const res = yield http.delete(`/webhook/${ID}`);
        yield put(developmentActions.deleteWebhookSuccess(ID));
        successMessage('Successfully deleted webhook');
    } catch (error) {
        console.log(error);
        const msg = error.response?.data?.msg || 'Couldn\'t delete webhook';
        yield put(developmentActions.deleteWebhookFailure(msg));
        errorMessage(msg);
    }
}


function* watchGetWebhookList() {
    yield takeLatest(actionTypes.FETCH_DEV_REQUEST, getWebhookList);
}


function* watchSaveWebhook() {
    yield takeLatest(actionTypes.SAVE_WEBHOOK_REQUEST, saveWebhook);
}

function* watchCreateWebhook() {
    yield takeLatest(actionTypes.CREATE_WEBHOOK_REQUEST, createWebhook);
}


function* watchDeleteWebhook() {
    yield takeLatest(actionTypes.DELETE_WEBHOOK_REQUEST, deleteWebhook);
}


export function* developmentSaga() {
    yield all([
        watchGetWebhookList(),
        watchSaveWebhook(),
        watchCreateWebhook(),
        watchDeleteWebhook()
    ]);
}
