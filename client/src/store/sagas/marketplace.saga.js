import {all, put, takeEvery} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {marketplaceActions} from "../actions";
import {errorMessage, http, loadingMessage, successMessage} from "helpers";


function* fetchMarketplace() {
    try {
        const res = yield http.get('/marketplace');
        successMessage(res.data?.msg || "Marketplace fetched successfully");
        yield put(marketplaceActions.fetchMarketplaceSuccess(res.data.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't fetch marketplace";
        errorMessage(msg);
        yield put(marketplaceActions.fetchMarketplaceFailure());
    }
}

function* pingMarketplace({marketplaceType}) {
    try {
        const res = yield http.get(`/marketplace/${marketplaceType}`);
        yield put(marketplaceActions.pingMarketplaceSuccess(res.data?.data.Status));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't ping marketplace";
        errorMessage(msg);
        yield put(marketplaceActions.pingMarketplaceFailure(msg));
    }
}

function* disconnectMarketplace({marketplaceType}) {
    try {
        const res = yield http.delete(`/marketplace/${marketplaceType}`);
        successMessage(res.data.msg || 'Marketplace is disconnected');
        yield put(marketplaceActions.disconnectMarketplaceSuccess());
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't disconnect marketplace";
        yield put(marketplaceActions.disconnectMarketplaceFailure(msg));
        errorMessage(msg);
    }
}

function* connectMarketplace({marketplaceType, auth}) {
    try {
        loadingMessage('Connecting to ' + marketplaceType, 0);
        const res = yield http.post(`/marketplace/connect`, {type: marketplaceType, auth});
        successMessage(res.data?.msg || `${marketplaceType} connected successfully`);
        yield put(marketplaceActions.connectMarketplaceSuccess());
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't Connect CRM";
        errorMessage(msg);
        yield put(marketplaceActions.connectMarketplaceFailure(msg));
    }
}

function* exportRecruiterValueReport({connectedCRM_Type}) {
    try {
        const res = yield http.post(`/crm/recruiter_value_report`, {crm_type: connectedCRM_Type.Name});
        yield put(marketplaceActions.exportRecruiterValueReportSuccess(res.data.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "An error has occurred";
        yield put(marketplaceActions.exportRecruiterValueReportFailure(msg));
        errorMessage(msg);
    }
}


function* watchPingMarketplace() {
    yield takeEvery(actionTypes.PING_MARKETPLACE_REQUEST, pingMarketplace)
}

function* watchFetchMarketplace() {
    yield takeEvery(actionTypes.FETCH_MARKETPLACE_REQUEST, fetchMarketplace)
}

function* watchConnectMarketplace() {
    yield takeEvery(actionTypes.CONNECT_MARKETPLACE_REQUEST, connectMarketplace)
}

function* watchDisconnectMarketplace() {
    yield takeEvery(actionTypes.DISCONNECT_MARKETPLACE_REQUEST, disconnectMarketplace)
}

function* watchExportRecruiterValueReport() {
    yield takeEvery(actionTypes.EXPORT_RECRUITER_VALUE_REPORT_REQUEST, exportRecruiterValueReport)
}


export function* marketplaceSaga() {
    yield all([
        watchPingMarketplace(),
        watchFetchMarketplace(),
        watchConnectMarketplace(),
        watchDisconnectMarketplace(),

        watchExportRecruiterValueReport()

    ])
}
