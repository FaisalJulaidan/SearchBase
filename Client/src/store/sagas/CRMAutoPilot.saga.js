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

function* fetchCRMAutoPilot({CRMAutoPilotID, meta}) {
    try {
        const res = yield http.get(`/crm_auto_pilot/${CRMAutoPilotID}`);
        yield put({...CRMAutoPilotActions.fetchCRMAutoPilotSuccess(res.data?.data), meta});

    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't load CRM auto pilot";
        yield put({...CRMAutoPilotActions.fetchCRMAutoPilotFailure(msg), meta});
        errorMessage(msg);
    }
}

function* addCRMAutoPilot({type, newCRMAutoPilot}) {
    try {
      console.log(newCRMAutoPilot)
        loadingMessage('Creating auto pilot...', 0);
        const res = yield http.post(`/crm_auto_pilots`, newCRMAutoPilot);
        yield put(CRMAutoPilotActions.addCRMAutoPilotSuccess(res.data?.data, res.data?.msg));
        successMessage('CRM Auto pilot added');

    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't create a new CRM auto pilot";
        yield put(CRMAutoPilotActions.addCRMAutoPilotFailure(msg));
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

function* updateCRMAutoPilotConfigs({CRMAutoPilotID, updatedValues}) {
    try {
        const res = yield http.put(`crm_auto_pilot/${CRMAutoPilotID}/configs`, updatedValues);
        yield put(CRMAutoPilotActions.updateCRMAutoPilotConfigsSuccess(res.data?.data, res.data?.msg));
        successMessage('CRM Auto pilot updated');
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't update auto pilot";
        yield put(CRMAutoPilotActions.updateCRMAutoPilotConfigsSuccess(msg));
        errorMessage(msg);
    }
}

function* deleteCRMAutoPilot({CRMAutoPilotID, meta}) {
    try {
        loadingMessage('Removing auto pilot...', 0);
        const res = yield http.delete(`/crm_auto_pilot/${CRMAutoPilotID}`);
        yield put({...CRMAutoPilotActions.deleteCRMAutoPilotSuccess(CRMAutoPilotID, res.data?.msg), meta});
        successMessage('CRM AutoPilot deleted');
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't delete CRM auto pilot";
        yield put({...CRMAutoPilotActions.deleteCRMAutoPilotFailure(msg), meta});
        errorMessage(msg);
    }
}

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

function* watchUpdateCRMAutoPilotConfigs() {
    yield takeLatest(actionTypes.UPDATE_CRM_AUTOPILOT_CONFIGS_REQUEST, updateCRMAutoPilotConfigs)
}

function* watchDeleteAutoPilot() {
    yield takeLatest(actionTypes.DELETE_CRM_AUTOPILOT_REQUEST, deleteCRMAutoPilot)
}

// function* watchUpdateStatus() {
//     yield takeLatest(actionTypes.UPDATE_AUTOPILOT_STATUS_REQUEST, updateStatus)
// }

export function* CRMAutoPilotSaga() {
    yield all([
        watchFetchCRMAutoPilots(),
        watchFetchCRMAutoPilot(),
        watchAddCRMAutoPilot(),
        watchUpdateCRMAutoPilot(),
        watchUpdateCRMAutoPilotConfigs(),
        watchDeleteAutoPilot()
        // watchUpdateAutoPilotConfigs(),
        // watchDeleteAutoPilot(),
        // watchUpdateStatus(),
    ])
}
