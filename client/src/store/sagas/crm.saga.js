import {all, put, takeEvery} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {crmActions} from "../actions";
import {destroyMessage, errorMessage, http, loadingMessage, successMessage} from "helpers";

function* fetchCRMs() {
    try {
        const res = yield http.get(`/crm`);
        yield put(crmActions.getConnectedCRMsSuccess(res.data?.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't load CRMs";
        errorMessage(msg);
        yield put(crmActions.getConnectedCRMsFailure());
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
        errorMessage(msg);
        yield put(crmActions.connectCrmFailure(msg));
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
        errorMessage(msg);
        yield put(crmActions.testCrmFailure(msg));
    }
}

function* disconnectCrm({disconnectedCRMID}) {
    try {
        const res = yield http.delete(`/crm/${disconnectedCRMID.ID}`);
        successMessage(res.data.msg || 'CRM Disconnected');
        yield put(crmActions.disconnectCrmSuccess(res.data.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't disconnect";
        yield put(crmActions.disconnectCrmFailure(msg));
        errorMessage(msg);
    }
}

function* exportRecruiterValueReport({connectedCRM_Type}) {
    try {
        const res = yield http.post(`/crm/recruiter_value_report`, {crm_type: connectedCRM_Type.Name});
        yield put(crmActions.exportRecruiterValueReportSuccess(res.data.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "An error has occurred";
        yield put(crmActions.exportRecruiterValueReportFailure(msg));
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
