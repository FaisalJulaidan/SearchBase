import {put, takeEvery,takeLatest, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {assistantActions, flowActions} from "../actions";
import {http, destroyMessage, loadingMessage, successMessage, errorMessage} from "../../helpers";


function* fetchAssistants() {
    try {
        const res = yield http.get(`/assistants`);
        yield put(assistantActions.fetchAssistantsSuccess(res.data.data));
    } catch (error) {
        console.log(error);
        errorMessage(error.response.data.msg);
        yield put(assistantActions.fetchAssistantsFailure(error.response.data));
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
        yield errorMessage("Couldn't create a new assistant");
        yield put(assistantActions.addAssistantFailure(error.response.data));
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
        errorMessage(error.response.data.msg);
        yield put(assistantActions.updateAssistantFailure(error.response.data));

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
        yield put(assistantActions.deleteAssistantFailure(error.response.data));
        errorMessage("Error in deleting assistant");
    }
}


function* updateFlow({assistant}) {
    try {
        loadingMessage('Updating Flow', 0);

        const res = yield http.put(`/assistant/${assistant.ID}/flow`, {flow: assistant.Flow});
        successMessage('Flow Updated');
        yield put(assistantActions.updateFlowSuccess(assistant, res.data.msg));
    } catch (error) {
        console.log(error);
        yield put(assistantActions.updateFlowFailure(error.response.data));
        errorMessage("Error in updating flow");
    }
}

function* updateStatus({status, assistantID}) {
    try {
        loadingMessage('Updating Status', 0);
        const res = yield http.put(`/assistant/${assistantID}/status`, {status});
        yield destroyMessage();
        yield successMessage('Status Updated');
        yield put(assistantActions.changeAssistantStatusSuccess('Status updated successfully',
                                                                            status, assistantID));
    } catch (error) {
        console.log(error);
        yield put(assistantActions.changeAssistantStatusFailure(error.response.data));
        yield destroyMessage();
        yield errorMessage("Error in updating assistant status");
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