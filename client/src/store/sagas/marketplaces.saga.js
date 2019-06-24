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

function* connectMarketplace({connectedCRM}) {
    try {
        loadingMessage('Connecting to ' + connectedCRM.type, 0);
        const res = yield http.post(`/crm/connect`, {type: connectedCRM.type, auth: connectedCRM.auth});
        successMessage(res.data?.msg || `${connectedCRM.type} connected successfully`);
        yield put(marketplacesActions.connectMarketplaceSuccess(res.data.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't Connect CRM";
        errorMessage(msg);
        yield put(marketplacesActions.connectMarketplaceFailure(msg));
    }
}

function* testMarketplace({testedCRM}) {
    const defaultMsg = "Couldn't Test CRM";
    try {
        loadingMessage('Connecting to ' + testedCRM.type, 0);
        const res = yield http.post(`/crm/test`, {type: testedCRM.type, auth: testedCRM.auth});
        destroyMessage();
        successMessage(res.data?.msg || defaultMsg);
        yield put(marketplacesActions.testMarketplaceSuccess());
    } catch (error) {
        const msg = error.response?.data?.msg || "Test CRM connection failed";
        errorMessage(msg);
        yield put(marketplacesActions.testMarketplaceFailure(msg));
    }
}

function* disconnectMarketplace({disconnectedCRMID}) {
    try {
        const res = yield http.delete(`/crm/${disconnectedCRMID.ID}`);
        successMessage(res.data.msg || 'CRM Disconnected');
        yield put(marketplacesActions.disconnectMarketplaceSuccess(res.data.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't disconnect";
        yield put(marketplacesActions.disconnectMarketplaceFailure(msg));
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

function* watchConnectMarketplace() {
    yield takeEvery(actionTypes.CONNECT_MARKETPLACE_REQUEST, connectMarketplace)
}

function* watchTestMarketplace() {
    yield takeEvery(actionTypes.TEST_MARKETPLACE_REQUEST, testMarketplace)
}

function* watchDisconnectMarketplace() {
    yield takeEvery(actionTypes.DISCONNECT_MARKETPLACE_REQUEST, disconnectMarketplace)
}

function* watchExportRecruiterValueReport() {
    yield takeEvery(actionTypes.EXPORT_RECRUITER_VALUE_REPORT_REQUEST, exportRecruiterValueReport)
}


export function* marketplacesSaga() {
    yield all([
        watchFetchMarketplaces(),
        watchConnectMarketplace(),
        watchTestMarketplace(),
        watchDisconnectMarketplace(),
        watchExportRecruiterValueReport()

    ])
}
