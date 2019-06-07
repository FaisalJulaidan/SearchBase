import {all, put, takeEvery} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {crmActions} from "../actions";
import {destroyMessage, errorHandler, errorMessage, http, loadingMessage, successMessage} from "helpers";
import * as Sentry from '@sentry/browser';

function* fetchCRMs() {
    try {
        const res = yield http.get(`/crm`);
        yield put(crmActions.getConnectedCRMsSuccess(res.data?.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't load CRMs";
        console.error(error);
        errorMessage(msg);
        yield put(crmActions.getConnectedCRMsFailure());
        errorHandler(error);
    }
}

function* connectCrm({connectedCRM}) {
    try {
        loadingMessage('Connecting to ' + connectedCRM.type, 0);
        const res = yield http.post(`/crm/connect`, {type: connectedCRM.type, auth: connectedCRM.auth});
        successMessage(res.data?.msg || `${connectedCRM.type} connected successfully`);
        yield put(crmActions.connectCrmSuccess(res.data.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't Connect CRM";
        console.error(error);
        errorMessage(msg);
        yield put(crmActions.connectCrmFailure(msg));
        errorHandler(error)
    }
}

function* testCrm({testedCRM}) {
    const defaultMsg = "Couldn't Test CRM";
    try {
        loadingMessage('Connecting to ' + testedCRM.type, 0);
        const res = yield http.post(`/crm/test`, {type: testedCRM.type, auth: testedCRM.auth});
        destroyMessage();
        successMessage(res.data?.msg || defaultMsg);
        yield put(crmActions.testCrmSuccess());
    } catch (error) {
        const msg = error.response?.data?.msg || "Test CRM connection failed";
        console.error(error);
        errorMessage(msg);
        yield put(crmActions.testCrmFailure(msg));
        errorHandler(error)
    }
}

function* disconnectCrm({disconnectedCRMID}) {
    let msg = "Couldn't disconnect";
    try {
        const res = yield http.delete(`/crm/${disconnectedCRMID.ID}`);

        if (!res.data?.success) {
            errorMessage(res.data?.msg || msg);
            yield put(crmActions.disconnectCrmFailure(msg));
        }

        if (res.data?.msg)
            successMessage(res.data.msg);

        yield put(crmActions.disconnectCrmSuccess(res.data.data));
    } catch (error) {
        msg = error.response?.data?.msg;
        console.error(error);
        yield put(crmActions.disconnectCrmFailure(msg));
        Sentry.captureException(error);
        errorMessage(msg);
    }
}

function* exportRecruiterValueReport({connectedCRM_Type}) {
    try {
        const res = yield http.post(`/crm/recruiter_value_report`, {crm_type: connectedCRM_Type.Name});
        yield put(crmActions.exportRecruiterValueReportSuccess(res.data.data));
    } catch (error) {
        let data = error.response?.data;
        yield put(crmActions.exportRecruiterValueReportFailure(data.msg || "An error has occurred"));
        if (!data.msg) errorHandler(error)
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

function* watchExportRecruiterValueReport() {
    yield takeEvery(actionTypes.EXPORT_RECRUITER_VALUE_REPORT_REQUEST, exportRecruiterValueReport)
}


export function* crmSaga() {
    yield all([
        watchFetchCRMs(),
        watchConnectCrm(),
        watchTestCrm(),
        watchDisconnectCrm(),
        watchExportRecruiterValueReport()

    ])
}
