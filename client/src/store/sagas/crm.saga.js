import {all, put, takeEvery} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {crmActions} from "../actions";
import {errorHandler, errorMessage, http, successMessage} from "helpers";
import * as Sentry from '@sentry/browser';

function* fetchCRMs() {
    const msg = "Couldn't load CRMs";
    try {
        const res = yield http.get(`/crm`);
        if (!res.data?.data)
            yield put(crmActions.getConnectedCRMsFailure(msg));

        yield put(crmActions.getConnectedCRMsSuccess(res.data?.data));
    } catch (error) {
        msg = error.response?.data?.msg;
        console.error(error);
        yield put(crmActions.getConnectedCRMsFailure(msg));
        Sentry.captureException(error);
        errorMessage(msg);
    }
}

function* connectCrm({connectedCRM}) {
    const defaultMsg = "Couldn't Connect CRM";
    try {
        const res = yield http.post(`/crm/connect`, {type: connectedCRM.type, auth: connectedCRM.auth});
        successMessage(res.data?.msg || defaultMsg);
        yield put(crmActions.connectCrmSuccess());
    } catch (error) {
        let data = error.response?.data;
        errorMessage(data.msg || defaultMsg);
        yield put(crmActions.connectCrmFailure(data.msg || defaultMsg));
        if (!data.msg) errorHandler(error)
    }
}

function* testCrm({testedCRM}) {
    const defaultMsg = "Couldn't Test CRM";
    try {
        const res = yield http.post(`/crm/test`, {type: testedCRM.type, auth: testedCRM.auth});
        successMessage(res.data?.msg || defaultMsg);
        yield put(crmActions.testCrmSuccess());
    } catch (error) {
        let data = error.response?.data;
        errorMessage(data.msg || defaultMsg);
        yield put(crmActions.testCrmFailure(data.msg || defaultMsg));
        if (!data.msg) errorHandler(error)
    }
}

function* disconnectCrm({disconnectedCRM}) {
    let msg = "Couldn't disconnect";
    try {
        const res = yield http.delete(`/crm/${disconnectedCRM.ID}`);

        if (!res.data?.success) {
            errorMessage(res.data?.msg || msg);
            yield put(crmActions.disconnectCrmFailure(msg));
        }

        if (res.data?.msg)
            successMessage(res.data.msg);

        yield put(crmActions.disconnectCrmSuccess('disconnect'));
    } catch (error) {
        msg = error.response?.data?.msg;
        console.error(error);
        yield put(crmActions.disconnectCrmFailure(msg));
        Sentry.captureException(error);
        errorMessage(msg);
    }
}

function* watchFetchCRMs() {
    yield takeEvery(actionTypes.GET_CONNECTED_CRMS_REQUEST, fetchCRMs)
}

function* watchConnectCrm() {
    yield takeEvery(actionTypes.CONNECT_CRM_REQUEST, connectCrm)
}

function* watchTestCrm() {
    yield takeEvery(actionTypes.TEST_CRM_REQUEST, testCrm)
}

function* watchDisconnectCrm() {
    yield takeEvery(actionTypes.DISCONNECT_CRM_REQUEST, disconnectCrm)
}


export function* crmSaga() {
    yield all([
        watchFetchCRMs(),
        watchConnectCrm(),
        watchTestCrm(),
        watchDisconnectCrm()

    ])
}
