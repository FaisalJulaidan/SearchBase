import {all, put, takeEvery, takeLatest} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {assistantActions, flowActions} from "../actions";
import {errorMessage, flow, http, loadingMessage, successMessage} from "helpers";

function* fetchAssistants() {
    try {
        const res = yield http.get(`/assistants`);
        yield put(assistantActions.fetchAssistantsSuccess(res.data?.data.assistants));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't load assistants";
        errorMessage(msg);
        yield put(assistantActions.fetchAssistantsFailure(msg));
    }
}

function* fetchAssistant({assistantID, meta}) {
    try {
        const res = yield http.get(`/assistant/${assistantID}`);
        yield put({...assistantActions.fetchAssistantSuccess(res.data?.data), meta});
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't load assistants";
        errorMessage(msg);
        yield put({...assistantActions.fetchAssistantFailure(msg), meta});
    }
}

function* addAssistant({type, newAssistant}) {
    try {
        loadingMessage('Building assistant...', 0);
        const res = yield http.post(`/assistants`, newAssistant);
        yield put(assistantActions.addAssistantSuccess(res.data?.data, res.data?.msg));
        successMessage('Assistant added');
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't create a new assistant";
        errorMessage(msg);
        yield put(assistantActions.addAssistantFailure(msg));
    }
}

function* updateAssistant({assistantID, updatedSettings}) {
    try {
        const res = yield http.put(`assistant/${assistantID}`, updatedSettings);
        yield put(assistantActions.updateAssistantSuccess(assistantID, res.data?.data, res.data?.msg));
        successMessage('Assistant updated');
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't update assistant";
        errorMessage(msg);
        yield put(assistantActions.updateAssistantFailure(msg));
    }
}

function* updateAssistantConfigs({assistantID, updatedSettings}) {
    try {
        const res = yield http.put(`assistant/${assistantID}/configs`, updatedSettings);
        yield put(assistantActions.updateAssistantConfigsSuccess(assistantID, res.data?.data, res.data?.msg));
        successMessage('Assistant configuration updated');
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't update assistant configuration";
        errorMessage(msg);
        yield put(assistantActions.updateAssistantConfigsFailure(msg));
    }
}

function* deleteAssistant({assistantID, meta}) {
    try {
        loadingMessage('Removing assistant...', 0);
        const res = yield http.delete(`/assistant/${assistantID}`);
        yield put({...assistantActions.deleteAssistantSuccess(assistantID, res.data?.msg), meta});
        successMessage('Assistant deleted');
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't delete assistant";
        errorMessage(msg);
        yield put({...assistantActions.deleteAssistantFailure(msg), meta});
    }
}

function* updateFlow({assistant, meta}) {
    try {
        loadingMessage('Updating script...', 0);
        const res = yield http.put(`/assistant/${assistant.ID}/flow`, {flow: flow.parse(assistant.Flow)});
        yield put({...assistantActions.updateFlowSuccess(assistant, res.data?.msg), meta});
        successMessage('Script updated');
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't update script";
        errorMessage(msg);
        yield put({...assistantActions.updateFlowFailure(msg), meta});
    }
}


function* updateStatus({status, assistantID}) {
    try {
        loadingMessage('Updating status...', 0);
        const res = yield http.put(`/assistant/${assistantID}/status`, {status});
        yield put(assistantActions.changeAssistantStatusSuccess('Status updated successfully',
            status, assistantID));
        yield successMessage('Status updated');

    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't update assistant's status";
        errorMessage(msg);
        yield put(assistantActions.changeAssistantStatusFailure(msg));
    }
}


function* connectAssistantCRM({assistantID, CRMID}) {
    try {
        const res = yield http.post(`/assistant/${assistantID}/crm`, {CRMID});
        yield put(assistantActions.connectToCRMSuccess(CRMID, res.data?.msg));
        successMessage("CRM connected successfully");
    } catch (error) {
        const msg = error.response?.data?.msg || "Can't connect to CRM";
        errorMessage(msg);
        yield put(assistantActions.connectToCRMFailure(msg));
    }
}

function* disconnectAssistantCRM({assistantID}) {
    try {
        const res = yield http.delete(`/assistant/${assistantID}/crm`);
        yield put(assistantActions.disconnectFromCRMSuccess(res.data?.msg));
        successMessage("CRM disconnected successfully");
    } catch (error) {
        const msg = error.response?.data?.msg || "Can't disconnect from CRM";
        errorMessage(msg);
        yield put(assistantActions.disconnectFromCRMFailure(msg));
    }
}


function* connectAssistantCalendar({assistantID, calendarID}) {
    try {
        const res = yield http.post(`/assistant/${assistantID}/calendar`, {calendarID});
        yield put(assistantActions.connectToCalendarSuccess(calendarID, res.data?.msg));
        successMessage("Calendar connected successfully");
    } catch (error) {
        const msg = error.response?.data?.msg || "Can't connect to calendar";
        errorMessage(msg);
        yield put(assistantActions.connectToCalendarFailure(msg));
    }
}

function* disconnectAssistantCalendar({assistantID}) {
    try {
        const res = yield http.delete(`/assistant/${assistantID}/calendar`);
        yield put(assistantActions.disconnectFromCalendarSuccess(res.data?.msg));
        successMessage("Calendar disconnected successfully");
    } catch (error) {
        const msg = error.response?.data?.msg || "Can't disconnect from calendar";
        errorMessage(msg);
        yield put(assistantActions.disconnectFromCalendarFailure(msg));
    }
}


function* connectAutoPilot({assistantID, autoPilotID}) {
    try {
        const res = yield http.post(`/assistant/${assistantID}/auto_pilot`, {AutoPilotID: autoPilotID});
        successMessage(res.data?.msg || 'Auto pilot connected successfully');
        yield put(assistantActions.connectToAutoPilotSuccess(autoPilotID));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't connect to this auto pilot";
        errorMessage(msg);
        yield put(assistantActions.connectToAutoPilotFailure(msg));
    }
}

function* disconnectAutoPilot({assistantID, autoPilotID}) {
    try {
        const res = yield http.delete(`/assistant/${assistantID}/auto_pilot`, {AutoPilotID: autoPilotID});
        successMessage(res.data?.msg || "Disconnected from auto pilot successfully");
        yield put(assistantActions.disconnectFromAutoPilotSuccess(res.data?.msg));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't disconnect from auto pilot";
        errorMessage(msg);
        yield put(assistantActions.disconnectFromAutoPilotFailure(msg));
    }
}

function* watchDisconnectAutoPilot() {
    yield takeEvery(actionTypes.DISCONNECT_ASSISTANT_FROM_AUTO_PILOT_REQUEST, disconnectAutoPilot)
}

function* watchConnectAutoPilot() {
    yield takeEvery(actionTypes.CONNECT_ASSISTANT_TO_AUTO_PILOT_REQUEST, connectAutoPilot)
}

function* watchConnectAssistantCrm() {
    yield takeEvery(actionTypes.CONNECT_ASSISTANT_TO_CRM_REQUEST, connectAssistantCRM)
}

function* watchDisconnectAssistantCrm() {
    yield takeEvery(actionTypes.DISCONNECT_ASSISTANT_FROM_CRM_REQUEST, disconnectAssistantCRM)
}

function* watchConnectAssistantCalendar() {
    yield takeEvery(actionTypes.CONNECT_ASSISTANT_TO_CALENDAR_REQUEST, connectAssistantCRM)
}

function* watchDisconnectAssistantCalendar() {
    yield takeEvery(actionTypes.DISCONNECT_ASSISTANT_FROM_CALENDAR_REQUEST, disconnectAssistantCRM)
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

function* watchFetchAssistant() {
    yield takeEvery(actionTypes.FETCH_ASSISTANT_REQUEST, fetchAssistant)
}

function* watchAddAssistant() {
    yield takeEvery(actionTypes.ADD_ASSISTANT_REQUEST, addAssistant)
}

function* watchUpdateAssistant() {
    yield takeEvery(actionTypes.UPDATE_ASSISTANT_REQUEST, updateAssistant)
}

function* watchUpdateAssistantConfigs() {
    yield takeEvery(actionTypes.UPDATE_ASSISTANT_CONFIGS_REQUEST, updateAssistantConfigs)
}

function* watchDeleteAssistant() {
    yield takeEvery(actionTypes.DELETE_ASSISTANT_REQUEST, deleteAssistant)
}




export function* assistantSaga() {
    yield all([

        watchFetchAssistants(),
        watchFetchAssistant(),
        watchAddAssistant(),
        watchUpdateAssistant(),
        watchUpdateAssistantConfigs(),
        watchDeleteAssistant(),
        watchUpdateFlow(),
        watchUpdateStatus(),

        watchConnectAssistantCrm(),
        watchDisconnectAssistantCrm(),

        watchConnectAssistantCalendar(),
        watchDisconnectAssistantCalendar(),


        watchConnectAutoPilot(),
        watchDisconnectAutoPilot()


    ])
}
