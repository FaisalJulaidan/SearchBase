import {put, takeEvery,takeLatest, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {assistantActions, flowActions} from "../actions";
import {http, loadingMessage, successMessage, errorMessage, flow} from "../../helpers";


function* fetchAssistants() {
    try {
        const res = yield http.get(`/assistants`);
        yield put(assistantActions.fetchAssistantsSuccess(res.data.data));
    } catch (error) {
        console.log(error);
        const msg = "Couldn't load assistants";
        yield put(assistantActions.fetchAssistantsFailure(msg));
        errorMessage(msg);
    }

}

function* addAssistant({type, newAssistant}) {
    try {
        loadingMessage('Creating assistant...', 0);
        const res = yield http.post(`/assistants`, newAssistant);
        yield put(assistantActions.addAssistantSuccess(res.data.msg));
        yield put(assistantActions.fetchAssistants());
        successMessage('Assistant added!');

    } catch (error) {
        console.log(error);
        const msg = "Couldn't create a new assistant";
        yield put(assistantActions.addAssistantFailure(msg));
        errorMessage(msg);
    }
}

function* updateAssistant({assistantID, updatedSettings}) {
    try {
        const res = yield http.put(`assistant/${assistantID}`, updatedSettings);
        yield put(assistantActions.updateAssistantSuccess(res.data.msg));
        yield put(assistantActions.fetchAssistants());
        successMessage('Assistant updated!');
    } catch (error) {
        console.log(error);
        const msg = "Couldn't update assistant";
        yield put(assistantActions.updateAssistantFailure(msg));
        errorMessage(msg);

    }
}


function* deleteAssistant({assistantID}) {
    try {
        loadingMessage('Removing assistant...', 0);
        const res = yield http.delete(`/assistant/${assistantID}`);
        yield put(assistantActions.deleteAssistantSuccess(assistantID, res.data.msg));
        successMessage('Assistant deleted');
    } catch (error) {
        console.log(error);
        const msg = "Couldn't delete assistant";
        yield put(assistantActions.deleteAssistantFailure(msg));
        errorMessage(msg);
    }
}


function* updateFlow({assistant}) {
    try {
        loadingMessage('Updating Flow', 0);
        const res = yield http.put(`/assistant/${assistant.ID}/flow`, {flow: flow.parse(assistant.Flow)});
        yield put(assistantActions.updateFlowSuccess(assistant, res.data.msg));
        successMessage('Flow updated');
    } catch (error) {
        console.log(error);
        const msg = "Couldn't update flow";
        yield put(assistantActions.updateFlowFailure(msg));
        errorMessage(msg);
    }
}

function* updateStatus({status, assistantID}) {
    try {
        loadingMessage('Updating Status', 0);
        const res = yield http.put(`/assistant/${assistantID}/status`, {status});
        yield put(assistantActions.changeAssistantStatusSuccess('Status updated successfully',
                                                                            status, assistantID));
        yield successMessage('Status Updated');

    } catch (error) {
        console.log(error);
        const msg = "Couldn't update assistant's status";
        yield put(assistantActions.changeAssistantStatusFailure(msg));
        errorMessage(msg);
    }
}


function* watchUpdateStatus() {
    yield takeLatest(actionTypes.CHANGE_ASSISTANT_STATUS_REQUEST, updateStatus)
}

function* watchUpdateFlow() {
    yield takeLatest(actionTypes.UPDATE_FLOW_REQUEST, updateFlow)
}

function* watchFetchAssistants() {
    yield takeEvery(actionTypes.FETCH_ASSISTANTS_REQUEST, fetchAssistants)
}

function* watchAddAssistant() {
    yield takeEvery(actionTypes.ADD_ASSISTANT_REQUEST, addAssistant)
}

function* watchUpdateAssistant() {
    yield takeEvery(actionTypes.UPDATE_ASSISTANT_REQUEST, updateAssistant)
}

function* watchDeleteAssistant() {
    yield takeEvery(actionTypes.DELETE_ASSISTANT_REQUEST, deleteAssistant)
}


export function* assistantSaga() {
    yield all([
        watchFetchAssistants(),
        watchAddAssistant(),
        watchUpdateAssistant(),
        watchDeleteAssistant(),
        watchUpdateFlow(),
        watchUpdateStatus(),
    ])
}