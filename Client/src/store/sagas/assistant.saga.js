import {all, put, takeEvery, takeLatest} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import { accountActions, assistantActions, flowActions } from '../actions';
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

        // Set logo path
        let assistant = res.data?.data;
        let file = assistant.StoredFile?.StoredFileInfo?.find(
            item => item.Key === 'Logo'
        );
        assistant.LogoPath = file?.AbsFilePath || null;

        yield put({...assistantActions.fetchAssistantSuccess(assistant), meta});
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't load assistants";
        errorMessage(msg);
        yield put({...assistantActions.fetchAssistantFailure(msg), meta});
    }
}

function* addAssistant({newAssistant}) {
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

function* connectToCRM({assistantID, CRMID}) {
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

function* disconnectFromCRM({assistantID}) {
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

function* connectToCalendar({assistantID, calendarID}) {
    try {
        const res = yield http.post(`/assistant/${assistantID}/calendar`, {calendarID});
        yield put(assistantActions.connectToCalendarSuccess(calendarID, res.data?.msg));
        successMessage("CalendarID connected successfully");
    } catch (error) {
        const msg = error.response?.data?.msg || "Can't connect to calendar";
        errorMessage(msg);
        yield put(assistantActions.connectToCalendarFailure(msg));
    }
}

function* disconnectFromCalendar({assistantID}) {
    try {
        const res = yield http.delete(`/assistant/${assistantID}/calendar`);
        yield put(assistantActions.disconnectFromCalendarSuccess(res.data?.msg));
        successMessage("Calendar disconnected successfully");
    } catch (error) {
        const msg = error.response?.data?.msg || "Can't disconnect from calendar";
        errorMessage(msg);
        yield put(assistantActions.disconnectFromCalendaFailure(msg));
    }
}

function* connectToMessenger({assistantID, messengerID}) {
    try {
        const res = yield http.post(`/assistant/${assistantID}/messenger`, {messengerID});
        yield put(assistantActions.connectToMessengerSuccess(messengerID, res.data?.msg));
        successMessage("SMS connected successfully");
    } catch (error) {
        const msg = error.response?.data?.msg || "Can't connect to SMS";
        errorMessage(msg);
        yield put(assistantActions.connectToMessengerFailure(msg));
    }
}

function* disconnectFromMessenger({assistantID}) {
    try {
        const res = yield http.delete(`/assistant/${assistantID}/messenger`);
        yield put(assistantActions.disconnectFromMessengerSuccess(res.data?.msg));
        successMessage("SMS disconnected successfully");
    } catch (error) {
        const msg = error.response?.data?.msg || "Can't disconnect from SMS";
        errorMessage(msg);
        yield put(assistantActions.disconnectFromMessengerFailure(msg));
    }
}

function* connectToAutoPilot({assistantID, autoPilotID}) {
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

function* disconnectFromAutoPilot({assistantID, autoPilotID}) {
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

function* uploadLogo({ assistantID, file }) {
    try {
        loadingMessage('Uploading logo', 0);
        const res = yield http.post(`/assistant/${assistantID}/logo`, file);
        yield successMessage('Logo uploaded');
        yield put(assistantActions.uploadLogoSuccess(res.data?.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't upload logo";
        errorMessage(msg);
        yield put(assistantActions.uploadLogoFailure(msg));
    }
}

function* deleteLogo({assistantID}) {
    try {
        loadingMessage('Deleting logo', 0);
        const res = yield http.delete(`/assistant/${assistantID}/logo`);
        successMessage('Logo deleted');
        yield put(assistantActions.deleteLogoSuccess());
    } catch (error) {
        const msg = error.response?.data?.msg || "Can't delete logo";
        errorMessage(msg);
        yield put(assistantActions.deleteLogoFailure(msg));
    }
}

function* watchUploadLogo() {
    yield takeEvery(actionTypes.UPLOAD_ASSISTANT_LOGO_REQUEST, uploadLogo);
}

function* watchDeleteLogo() {
    yield takeEvery(actionTypes.DELETE_ASSISTANT_LOGO_REQUEST, deleteLogo);
}

function* watchDisconnectAutoPilot() {
    yield takeEvery(actionTypes.DISCONNECT_ASSISTANT_FROM_AUTO_PILOT_REQUEST, disconnectFromAutoPilot)
}

function* watchConnectAutoPilot() {
    yield takeEvery(actionTypes.CONNECT_ASSISTANT_TO_AUTO_PILOT_REQUEST, connectToAutoPilot)
}

function* watchDisconnectMessenger() {
    yield takeEvery(actionTypes.DISCONNECT_ASSISTANT_FROM_MESSENGER_REQUEST, disconnectFromMessenger)
}

function* watchConnectMessenger() {
    yield takeEvery(actionTypes.CONNECT_ASSISTANT_TO_MESSENGER_REQUEST, connectToMessenger)
}

function* watchConnectAssistantCrm() {
    yield takeEvery(actionTypes.CONNECT_ASSISTANT_TO_CRM_REQUEST, connectToCRM)
}

function* watchDisconnectFromCrm() {
    yield takeEvery(actionTypes.DISCONNECT_ASSISTANT_FROM_CRM_REQUEST, disconnectFromCRM)
}

function* watchConnectToCalendar() {
    yield takeEvery(actionTypes.CONNECT_ASSISTANT_TO_CALENDAR_REQUEST, connectToCalendar)
}

function* watchDisconnectAssistantCalendar() {
    yield takeEvery(actionTypes.DISCONNECT_ASSISTANT_FROM_CALENDAR_REQUEST, disconnectFromCalendar)
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
        watchDisconnectFromCrm(),

        watchConnectToCalendar(),
        watchDisconnectAssistantCalendar(),

        watchDisconnectMessenger(),
        watchConnectMessenger(),


        watchConnectAutoPilot(),
        watchDisconnectAutoPilot(),

        watchUploadLogo(),
        watchDeleteLogo(),
    ])
}
