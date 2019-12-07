import {all, put, takeEvery} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {marketplaceActions} from "../actions";
import {errorMessage, http, loadingMessage, successMessage} from "helpers";


function* fetchMarketplace() {
    try {
        const res = yield http.get('/marketplace');
        yield put(marketplaceActions.fetchMarketplaceSuccess(res.data.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't fetch your connected marketplace items";
        errorMessage(msg);
        yield put(marketplaceActions.fetchMarketplaceFailure());
    }
}

function* fetchMarketplaceItem({marketplaceType}) {
    try {
        const res = yield http.get(`/marketplace/${marketplaceType}/fetch`);
        yield put(marketplaceActions.fetchMarketplaceItemSuccess(res.data.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't fetch marketplace item";
        errorMessage(msg);
        yield put(marketplaceActions.fetchMarketplaceItemFailure());
    }
}

function* saveMarketplaceItem({marketplaceType, CRMAutoPilotID}) {
    try {
        const res = yield http.post(`/marketplace/${marketplaceType}/save`, {CRMAutoPilotID});
        successMessage(`Saved settings succesfully`);
        yield put(marketplaceActions.saveMarketplaceItemSuccess(res.data.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't save marketplace item";
        errorMessage(msg);
        yield put(marketplaceActions.saveMarketplaceItemFailure());
    }
}


function* pingMarketplace({marketplaceType, meta}) {
    try {
        const res = yield http.get(`/marketplace/${marketplaceType}`);
        yield put({...marketplaceActions.pingMarketplaceSuccess(res.data?.data.Status), meta});
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't ping marketplace";
        errorMessage(msg);
        yield put({...marketplaceActions.pingMarketplaceFailure(msg), meta});
    }
}

function* disconnectMarketplace({marketplaceType}) {
    try {
        const res = yield http.delete(`/marketplace/${marketplaceType}`);
        successMessage(`${marketplaceType} is disconnected successfully`);
        yield put(marketplaceActions.disconnectMarketplaceSuccess());
    } catch (error) {
        const msg = error.response?.data?.msg || `Couldn't disconnect ${marketplaceType}`;
        yield put(marketplaceActions.disconnectMarketplaceFailure(msg));
        errorMessage(msg);
    }
}

function* connectMarketplace({marketplaceType, auth}) {
    try {
        loadingMessage('Connecting to ' + marketplaceType, 0);
        const res = yield http.post(`/marketplace/connect`, {type: marketplaceType, auth});
        successMessage(`${marketplaceType} connected successfully`);
        yield put(marketplaceActions.connectMarketplaceSuccess());
    } catch (error) {
        const msg = error.response?.data?.msg || `Couldn't Connect ${marketplaceType}`;
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

function* watchSaveMarketplaceItem(){
    yield takeEvery(actionTypes.SAVE_MARKETPLACE_ITEM_REQUEST, saveMarketplaceItem)
}

function* watchFetchItemMarketplace() {
    yield takeEvery(actionTypes.FETCH_MARKETPLACE_ITEM_REQUEST, fetchMarketplaceItem)
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
        watchSaveMarketplaceItem(),
        watchFetchItemMarketplace(),
        watchExportRecruiterValueReport()

    ])
}
