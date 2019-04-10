import {put, takeEvery, takeLatest, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {assistantActions, flowActions} from "../actions";
import {http, loadingMessage, successMessage, errorMessage, flow} from "helpers";


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
        loadingMessage('Updating Script', 0);
        const res = yield http.put(`/assistant/${assistant.ID}/flow`, {flow: flow.parse(assistant.Flow)});
        yield put(assistantActions.updateFlowSuccess(assistant, res.data.msg));
        successMessage('Script updated!');
    } catch (error) {
        console.log(error);
        const msg = "Couldn't update script";
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

function* connectCRM({CRM, assistant}) {
    try {
        loadingMessage('Connecting to ' + CRM.type, 0);
        const res = yield http.post(`/assistant/${assistant.ID}/crm/connect`, {...CRM});
        yield put(assistantActions.connectCRMSuccess({}, res.data.msg));
        // yield put(assistantActions.fetchAssistants());
        yield successMessage('Connected successfully to ' + CRM.type);
    } catch (error) {
        console.error(error);
        const msg = 'CRM API Error:' + error.response.data.msg;
        yield put(assistantActions.connectCRMFailure(msg), 3.5);
        errorMessage(msg);
    }
}

function* testCRM({CRM, assistant}) {
    try {
        loadingMessage('Testing ' + CRM.type, 0);
        const res = yield http.post(`/assistant/${assistant.ID}/crm/test`, {...CRM});
        yield put(assistantActions.testCRMSuccess({}, res.data.msg));
        yield successMessage('Tested successfully ' + CRM.type);
    } catch (error) {
        console.error(error);
        const msg = 'CRM API Error:' + error.response.data.msg;
        yield put(assistantActions.testCRMFailure(msg));
        errorMessage(msg, 3.5);
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

function* watchConnectCRM() {
    yield takeEvery(actionTypes.CONNECT_CRM_REQUEST, connectCRM)
}

function* watchTestCRM() {
    yield takeEvery(actionTypes.TEST_CRM_REQUEST, testCRM)
}


export function* assistantSaga() {
    yield all([
        watchFetchAssistants(),
        watchAddAssistant(),
        watchUpdateAssistant(),
        watchDeleteAssistant(),
        watchUpdateFlow(),
        watchUpdateStatus(),
        watchConnectCRM(),
        watchTestCRM(),
    ])
}
