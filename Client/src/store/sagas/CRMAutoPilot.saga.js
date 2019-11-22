import {all, put, takeLatest} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {CRMAutoPilotActions, autoPilotActions} from "../actions";
import {errorMessage, http, loadingMessage, successMessage} from "helpers";

function* fetchCRMAutoPilots() {
    try {
        const res = yield http.get(`/crm_auto_pilots`);
        yield put(CRMAutoPilotActions.fetchCRMAutoPilotsSuccess(res.data?.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't load CRM auto pilots";
        yield put(CRMAutoPilotActions.fetchCRMAutoPilotsFailure(msg));
        errorMessage(msg);
    }
}

function* fetchCRMAutoPilot({autoPilotID, meta}) {
    try {
        const res = yield http.get(`/auto_pilot/${autoPilotID}`);
        yield put({...autoPilotActions.fetchAutoPilotSuccess(res.data?.data), meta});

    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't load CRM auto pilot";
        yield put({...autoPilotActions.fetchAutoPilotFailure(msg), meta});
        errorMessage(msg);
    }
}

function* addCRMAutoPilot({type, newAutoPilot}) {
    try {
        loadingMessage('Creating auto pilot...', 0);
        const res = yield http.post(`/auto_pilots`, newAutoPilot);
        yield put(autoPilotActions.addAutoPilotSuccess(res.data?.data, res.data?.msg));
        successMessage('Auto pilot added');

    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't create a new auto pilot";
        yield put(autoPilotActions.addAutoPilotFailure(msg));
        errorMessage(msg);
    }
}

function* updateCRMAutoPilot({CRMAutoPilotID, updatedValues}) {
    try {
        const res = yield http.put(`crm_auto_pilot/${CRMAutoPilotID}`, updatedValues);
        yield put(CRMAutoPilotActions.updateCRMAutoPilotSuccess(CRMAutoPilotID, res.data?.data, res.data?.msg));
        successMessage('CRM Auto pilot updated');
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't update CRM auto pilot";
        yield put(CRMAutoPilotActions.updateCRMAutoPilotFailure(msg));
        errorMessage(msg);
    }
}

// function* updateAutoPilotConfigs({autoPilotID, updatedValues}) {
//     try {
//         const res = yield http.put(`auto_pilot/${autoPilotID}/configs`, updatedValues);
//         yield put(autoPilotActions.updateAutoPilotConfigsSuccess(res.data?.data, res.data?.msg));
//         successMessage('Auto pilot updated');
//     } catch (error) {
//         const msg = error.response?.data?.msg || "Couldn't update auto pilot";
//         yield put(autoPilotActions.updateAutoPilotConfigsFailure(msg));
//         errorMessage(msg);
//     }
// }

// function* deleteAutoPilot({autoPilotID, meta}) {
//     try {
//         loadingMessage('Removing auto pilot...', 0);
//         const res = yield http.delete(`/auto_pilot/${autoPilotID}`);
//         yield put({...autoPilotActions.deleteAutoPilotSuccess(autoPilotID, res.data?.msg), meta});
//         successMessage('AutoPilot deleted');
//     } catch (error) {
//         const msg = error.response?.data?.msg || "Couldn't delete auto pilot";
//         yield put({...autoPilotActions.deleteAutoPilotFailure(msg), meta});
//         errorMessage(msg);
//     }
// }

// function* updateStatus({status, autoPilotID}) {
//     try {
//         loadingMessage('Updating Status', 0);
//         const res = yield http.put(`/auto_pilot/${autoPilotID}/status`, {status});
//         yield put(autoPilotActions.updateAutoPilotSuccess('Status updated successfully', status, autoPilotID));
//         yield successMessage('Status updated');

//     } catch (error) {
//         const msg = error.response?.data?.msg || "Couldn't update assistant's status";
//         yield put(autoPilotActions.updateAutoPilotFailure(msg));
//         errorMessage(msg);
//     }
// }

function* watchFetchCRMAutoPilots() {
    yield takeLatest(actionTypes.FETCH_CRM_AUTOPILOTS_REQUEST, fetchCRMAutoPilots)
}

function* watchFetchCRMAutoPilot() {
    yield takeLatest(actionTypes.FETCH_CRM_AUTOPILOT_REQUEST, fetchCRMAutoPilot)
}

function* watchAddCRMAutoPilot() {
    yield takeLatest(actionTypes.ADD_CRM_AUTOPILOT_REQUEST, addCRMAutoPilot)
}

function* watchUpdateCRMAutoPilot() {
    yield takeLatest(actionTypes.UPDATE_CRM_AUTOPILOT_REQUEST, updateCRMAutoPilot)
}

// function* watchUpdateAutoPilotConfigs() {
//     yield takeLatest(actionTypes.UPDATE_AUTOPILOT_CONFIGS_REQUEST, updateAutoPilotConfigs)
// }

// function* watchDeleteAutoPilot() {
//     yield takeLatest(actionTypes.DELETE_AUTOPILOT_REQUEST, deleteAutoPilot)
// }

// function* watchUpdateStatus() {
//     yield takeLatest(actionTypes.UPDATE_AUTOPILOT_STATUS_REQUEST, updateStatus)
// }

export function* CRMAutoPilotSaga() {
    yield all([
        watchFetchCRMAutoPilots(),
        watchFetchCRMAutoPilot(),
        watchAddCRMAutoPilot(),
        watchUpdateCRMAutoPilot(),
        // watchUpdateAutoPilot(),
        // watchUpdateAutoPilotConfigs(),
        // watchDeleteAutoPilot(),
        // watchUpdateStatus(),
    ])
}
