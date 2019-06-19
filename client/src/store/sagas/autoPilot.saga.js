import {all, put, takeLatest} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {autoPilotActions} from "../actions";
import {errorMessage, http, loadingMessage, successMessage} from "helpers";

function* fetchAutoPilots() {
    try {
        const res = yield http.get(`/auto_pilots`);
        yield put(autoPilotActions.fetchAutoPilotsSuccess(res.data?.data));

    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't load auto pilots";
        yield put(autoPilotActions.fetchAutoPilotsFailure(msg));
        errorMessage(msg);
    }
}

function* fetchAutoPilot({autoPilotID, meta}) {
    try {
        const res = yield http.get(`/auto_pilot/${autoPilotID}`);
        yield put({...autoPilotActions.fetchAutoPilotSuccess(res.data?.data), meta});

    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't load auto pilots";
        yield put({...autoPilotActions.fetchAutoPilotFailure(msg), meta});
        errorMessage(msg);
    }
}

function* addAutoPilot({type, newAutoPilot}) {
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

function* updateAutoPilot({autoPilotID, updatedValues}) {
    try {
        const res = yield http.put(`auto_pilot/${autoPilotID}`, updatedValues);
        yield put(autoPilotActions.updateAutoPilotSuccess(autoPilotID, res.data?.data, res.data?.msg));
        successMessage('Auto pilot updated');
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't update auto pilot";
        yield put(autoPilotActions.updateAutoPilotFailure(msg));
        errorMessage(msg);
    }
}

function* updateAutoPilotConfigs({autoPilotID, updatedValues}) {
    try {
        const res = yield http.put(`auto_pilot/${autoPilotID}/configs`, updatedValues);
        yield put(autoPilotActions.updateAutoPilotConfigsSuccess(res.data?.data, res.data?.msg));
        successMessage('Auto pilot updated');
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't update auto pilot";
        yield put(autoPilotActions.updateAutoPilotConfigsFailure(msg));
        errorMessage(msg);
    }
}

function* deleteAutoPilot({autoPilotID, meta}) {
    try {
        loadingMessage('Removing auto pilot...', 0);
        const res = yield http.delete(`/auto_pilot/${autoPilotID}`);
        yield put({...autoPilotActions.deleteAutoPilotSuccess(autoPilotID, res.data?.msg), meta});
        successMessage('AutoPilot deleted');
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't delete auto pilot";
        yield put({...autoPilotActions.deleteAutoPilotFailure(msg), meta});
        errorMessage(msg);
    }
}

function* updateStatus({status, autoPilotID}) {
    try {
        loadingMessage('Updating Status', 0);
        const res = yield http.put(`/auto_pilot/${autoPilotID}/status`, {status});
        yield put(autoPilotActions.updateAutoPilotSuccess('Status updated successfully', status, autoPilotID));
        yield successMessage('Status updated');

    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't update assistant's status";
        yield put(autoPilotActions.updateAutoPilotFailure(msg));
        errorMessage(msg);
    }
}

function* watchFetchAutoPilots() {
    yield takeLatest(actionTypes.FETCH_AUTOPILOTS_REQUEST, fetchAutoPilots)
}

function* watchFetchAutoPilot() {
    yield takeLatest(actionTypes.FETCH_AUTOPILOT_REQUEST, fetchAutoPilot)
}

function* watchAddAutoPilot() {
    yield takeLatest(actionTypes.ADD_AUTOPILOT_REQUEST, addAutoPilot)
}

function* watchUpdateAutoPilot() {
    yield takeLatest(actionTypes.UPDATE_AUTOPILOT_REQUEST, updateAutoPilot)
}

function* watchUpdateAutoPilotConfigs() {
    yield takeLatest(actionTypes.UPDATE_AUTOPILOT_CONFIGS_REQUEST, updateAutoPilotConfigs)
}

function* watchDeleteAutoPilot() {
    yield takeLatest(actionTypes.DELETE_AUTOPILOT_REQUEST, deleteAutoPilot)
}

function* watchUpdateStatus() {
    yield takeLatest(actionTypes.UPDATE_AUTOPILOT_STATUS_REQUEST, updateStatus)
}

export function* autoPilotSaga() {
    yield all([
        watchFetchAutoPilots(),
        watchFetchAutoPilot(),
        watchAddAutoPilot(),
        watchUpdateAutoPilot(),
        watchUpdateAutoPilotConfigs(),
        watchDeleteAutoPilot(),
        watchUpdateStatus(),
    ])
}
