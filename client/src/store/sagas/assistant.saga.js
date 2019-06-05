import {all, put, takeEvery, takeLatest} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {assistantActions, crmActions, flowActions} from "../actions";
import {errorHandler, errorMessage, flow, http, loadingMessage, successMessage} from "helpers";
import * as Sentry from '@sentry/browser';

function* fetchAssistants() {
    try {
        const res = yield http.get(`/assistants`);
        yield put(crmActions.getConnectedCRMs());

        if (!res.data?.data)
            throw Error(`Can't fetch assistants`);

        yield put(assistantActions.fetchAssistantsSuccess(res.data?.data.assistants));
    } catch (error) {
        console.error(error);
        const msg = "Couldn't load assistants";
        yield put(assistantActions.fetchAssistantsFailure(msg));
        errorMessage(msg);
    }
}

function* addAssistant({type, newAssistant}) {
    try {
        loadingMessage('Building assistant...', 0);
        const res = yield http.post(`/assistants`, newAssistant);
        yield put(assistantActions.addAssistantSuccess(res.data?.data, res.data?.msg));
        successMessage('Assistant added');

    } catch (error) {
        console.error(error);
        const msg = "Couldn't create a new assistant";
        yield put(assistantActions.addAssistantFailure(msg));
        errorMessage(msg);
    }
}

function* updateAssistant({assistantID, updatedSettings}) {
    try {
        const res = yield http.put(`assistant/${assistantID}`, updatedSettings);
        yield put(assistantActions.updateAssistantSuccess(assistantID, res.data?.data, res.data?.msg));
        successMessage('Assistant updated');
    } catch (error) {
        console.error(error);
        const msg = "Couldn't update assistant";
        yield put(assistantActions.updateAssistantFailure(msg));
        errorMessage(msg);
    }
}


function* deleteAssistant({assistantID}) {
    try {
        loadingMessage('Removing assistant...', 0);
        const res = yield http.delete(`/assistant/${assistantID}`);
        yield put(assistantActions.deleteAssistantSuccess(assistantID, res.data?.msg));
        successMessage('Assistant deleted');
    } catch (error) {
        console.error(error);
        const msg = "Couldn't delete assistant";
        yield put(assistantActions.deleteAssistantFailure(msg));
        errorMessage(msg);
    }
}


function* updateFlow({assistant}) {
    try {
        loadingMessage('Updating script...', 0);
        const res = yield http.put(`/assistant/${assistant.ID}/flow`, {flow: flow.parse(assistant.Flow)});
        yield put(assistantActions.updateFlowSuccess(assistant, res.data?.msg));
        successMessage('Script updated');
    } catch (error) {
        console.error(error);
        const msg = "Couldn't update script";
        yield put(assistantActions.updateFlowFailure(msg));
        errorMessage(msg);
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
        console.error(error);
        const msg = "Couldn't update assistant's status";
        yield put(assistantActions.changeAssistantStatusFailure(msg));
        errorMessage(msg);
    }
}


function* selectAssistantCRM({assistantID, CRMID}) {
    let msg = "Can't select CRM";
    try {
        const res = yield http.post(`/assistant/${assistantID}/crm`, {CRMID});
        yield put(assistantActions.fetchAssistants());

        if (!res.data?.success) {
            errorMessage(res.data?.msg || msg);
            yield put(assistantActions.selectAssistantCRMFailure(msg));
        }

        if (res.data?.msg)
            successMessage(res.data.msg);

        yield put(assistantActions.selectAssistantCRMSuccess(res.data.data));
    } catch (error) {
        msg = error.response?.data?.msg;
        console.error(error);
        yield put(assistantActions.selectAssistantCRMFailure(msg));
        Sentry.captureException(error);
        errorMessage(msg);
    }
}

function* resetAssistantCRM({assistantID}) {
    let msg = "Can't reset CRM";
    try {
        const res = yield http.delete(`/assistant/${assistantID}/crm`);
        yield put(assistantActions.fetchAssistants());

        if (!res.data?.success) {
            errorMessage(res.data?.msg || msg);
            yield put(assistantActions.resetAssistantCRMFailure(msg));
        }

        if (res.data?.msg)
            successMessage(res.data.msg);

        yield put(assistantActions.resetAssistantCRMSuccess(res.data.data));
    } catch (error) {
        msg = error.response?.data?.msg;
        console.error(error);
        yield put(assistantActions.resetAssistantCRMFailure(msg));
        Sentry.captureException(error);
        errorMessage(msg);
    }
}


function* selectAutoPilot({assistantID, autoPilotID}) {
    try {
        const res = yield http.post(`/assistant/${assistantID}/auto_pilot`, {AutoPilotID: autoPilotID});
        successMessage(res.data?.msg || 'Auto pilot connected successfully');
        yield put(assistantActions.selectAutoPilotSuccess(assistantID, autoPilotID));
    } catch (error) {
        const defaultMsg = "Couldn't connect to this auto pilot";
        let data = error.response?.data;
        errorMessage(data.msg || defaultMsg);
        yield put(assistantActions.selectAutoPilotFailure(data.msg || defaultMsg));
        if (!data.msg) errorHandler(error)
    }
}

function* disconnectAutoPilot({assistantID, autoPilotID}) {
    try {
        const res = yield http.delete(`/assistant/${assistantID}/auto_pilot`, {AutoPilotID: autoPilotID});
        successMessage(res.data?.msg || "Disconnected from auto pilot successfuly");
        yield put(assistantActions.disconnectAutoPilotSuccess(assistantID, autoPilotID));
    } catch (error) {
        const defaultMsg = "CHANGE THIS";
        let data = error.response?.data;
        errorMessage(data.msg || defaultMsg);
        yield put(assistantActions.disconnectAutoPilotFailure(data.msg || defaultMsg));
        if (!data.msg) errorHandler(error)
    }
}

function* watchDisconnectAutoPilot() {
    yield takeEvery(actionTypes.DISCONNECT_AUTO_PILOT_REQUEST, disconnectAutoPilot)
}


function* watchSelectAutoPilot() {
    yield takeEvery(actionTypes.SELECT_AUTO_PILOT_REQUEST, selectAutoPilot)
}


function* watchResetAssistantCrm() {
    yield takeEvery(actionTypes.RESET_ASSISTANT_CRM_REQUEST, resetAssistantCRM)
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

function* watchSelectAssistantCrm() {
    yield takeEvery(actionTypes.SELECT_ASSISTANT_CRM_REQUEST, selectAssistantCRM)
}


export function* assistantSaga() {
    yield all([
        watchFetchAssistants(),
        watchAddAssistant(),
        watchUpdateAssistant(),
        watchDeleteAssistant(),
        watchUpdateFlow(),
        watchUpdateStatus(),
        watchSelectAssistantCrm(),
        watchResetAssistantCrm(),
        watchSelectAutoPilot(),
        watchDisconnectAutoPilot()


    ])
}
