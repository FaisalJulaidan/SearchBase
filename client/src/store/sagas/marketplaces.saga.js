import {all, put, takeEvery} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {marketplacesActions} from "../actions";
import {destroyMessage, errorMessage, http, loadingMessage, successMessage} from "helpers";

function* fetchMarketplaces() {
    try {
        const res = yield http.get(`/crm`);
        yield put(marketplacesActions.getConnectedCRMsSuccess(res.data?.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't load CRMs";
        errorMessage(msg);
        yield put(marketplacesActions.getConnectedCRMsFailure());
    }
}

function* connectCrm({connectedCRM}) {
    try {
        loadingMessage('Connecting to ' + connectedCRM.type, 0);
        const res = yield http.post(`/crm/connect`, {type: connectedCRM.type, auth: connectedCRM.auth});
        successMessage(res.data?.msg || `${connectedCRM.type} connected successfully`);
        yield put(marketplacesActions.connectCrmSuccess(res.data.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't Connect CRM";
        errorMessage(msg);
        yield put(marketplacesActions.connectCrmFailure(msg));
    }
}

function* testCrm({testedCRM}) {
    const defaultMsg = "Couldn't Test CRM";
    try {
        loadingMessage('Connecting to ' + testedCRM.type, 0);
        const res = yield http.post(`/crm/test`, {type: testedCRM.type, auth: testedCRM.auth});
        destroyMessage();
        successMessage(res.data?.msg || defaultMsg);
        yield put(marketplacesActions.testCrmSuccess());
    } catch (error) {
        const msg = error.response?.data?.msg || "Test CRM connection failed";
        errorMessage(msg);
        yield put(marketplacesActions.testCrmFailure(msg));
    }
}

function* disconnectCrm({disconnectedCRMID}) {
    try {
        const res = yield http.delete(`/crm/${disconnectedCRMID.ID}`);
        successMessage(res.data.msg || 'CRM Disconnected');
        yield put(marketplacesActions.disconnectCrmSuccess(res.data.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't disconnect";
        yield put(marketplacesActions.disconnectCrmFailure(msg));
        errorMessage(msg);
    }
}

function* exportRecruiterValueReport({connectedCRM_Type}) {
    try {
        const res = yield http.post(`/crm/recruiter_value_report`, {crm_type: connectedCRM_Type.Name});
        yield put(marketplacesActions.exportRecruiterValueReportSuccess(res.data.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "An error has occurred";
        yield put(marketplacesActions.exportRecruiterValueReportFailure(msg));
        errorMessage(msg);
    }
}

function* watchFetchMarketplaces() {
    yield takeEvery(actionTypes.GET_MARKETPLACES_REQUEST, fetchMarketplaces)
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


export function* marketplacesSaga() {
    yield all([
        watchFetchMarketplaces(),
        watchConnectCrm(),
        watchTestCrm(),
        watchDisconnectCrm(),
        watchExportRecruiterValueReport()

    ])
}
