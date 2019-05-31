import {all, put, takeEvery} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {autoPilotActions} from "../actions";
import {destroyMessage, errorHandler, errorMessage, flow, http, loadingMessage, successMessage} from "helpers";

function* fetchAutoPilots() {
    try {
        const res = yield http.get(`/auto_pilots`);
        if (!res.data?.data)
            throw Error(`Can't fetch auto pilots`);
        yield put(autoPilotActions.fetchAutoPilotsSuccess(res.data?.data));

    } catch (error) {
        console.error(error);
        const msg = "Couldn't load auto pilots";
        yield put(autoPilotActions.fetchAutoPilotsFailure(msg));
        errorMessage(msg);
    }
}

function* watchFetchAutoPilots() {
    yield takeEvery(actionTypes.FETCH_AUTOPILOTS_REQUEST, fetchAutoPilots)
}

function* addAutoPilot({type, newAutoPilot}) {
    try {
        loadingMessage('Creating auto pilot...', 0);
        const res = yield http.post(`/auto_pilots`, newAutoPilot);
        yield put(autoPilotActions.addAutoPilotSuccess(res.data?.data, res.data?.msg));
        successMessage('Auto pilot added');

    } catch (error) {
        console.error(error);
        const msg = "Couldn't create a new auto pilot";
        yield put(autoPilotActions.addAutoPilotFailure(msg));
        errorMessage(msg);
    }
}

function* watchAddAutoPilot() {
    yield takeEvery(actionTypes.ADD_AUTOPILOT_REQUEST, addAutoPilot)
}

function* updateAutoPilot({authPilotID, updatedValues}) {
    try {
        const res = yield http.put(`auto_pilot/${authPilotID}`, updatedValues);
        yield put(autoPilotActions.updateAutoPilotSuccess(authPilotID, res.data?.data, res.data?.msg));
        successMessage('Auto pilot updated');
    } catch (error) {
        console.error(error);
        const msg = "Couldn't update auto pilot";
        yield put(autoPilotActions.updateAutoPilotFailure(msg));
        errorMessage(msg);
    }
}

function* watchUpdateAutoPilot() {
    yield takeEvery(actionTypes.UPDATE_AUTOPILOT_REQUEST, updateAutoPilot)
}


function* deleteAutoPilot({authPilotID}) {
    try {
        loadingMessage('Removing auto pilot...', 0);
        const res = yield http.delete(`/auto_pilot/${authPilotID}`);
        yield put(autoPilotActions.deleteAutoPilotSuccess(authPilotID, res.data?.msg));
        successMessage('AutoPilot deleted');
    } catch (error) {
        console.error(error);
        const msg = "Couldn't delete auto pilot";
        yield put(autoPilotActions.deleteAutoPilotFailure(msg));
        errorMessage(msg);
    }
}


function* watchDeleteAutoPilot() {
    yield takeEvery(actionTypes.DELETE_AUTOPILOT_REQUEST, deleteAutoPilot)
}

export function* autoPilotSaga() {
    yield all([
        watchFetchAutoPilots(),
        watchAddAutoPilot(),
        watchUpdateAutoPilot(),
        watchDeleteAutoPilot(),
    ])
}
