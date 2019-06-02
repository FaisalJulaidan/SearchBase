import {all, put, takeEvery, takeLatest} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {assistantActions, crmActions, flowActions} from "../actions";
import {destroyMessage, errorHandler, errorMessage, flow, http, loadingMessage, successMessage} from "helpers";
import * as Sentry from '@sentry/browser';

function* fetchAssistants() {
    try {
        const res = yield http.get(`/assistants`);
        yield put(crmActions.getConnectedCRMs());

        if (!res.data?.data)
            throw Error(`Can't fetch assistants`);
        yield put(assistantActions.fetchAssistantsSuccess(res.data?.data));
    } catch (error) {
        console.error(error);
        const msg = "Couldn't load assistants";
        yield put(assistantActions.fetchAssistantsFailure(msg));
        errorMessage(msg);
    }

}

function* addAssistant({type, newAssistant}) {
    try {
        loadingMessage('Creating assistant...', 0);
        const res = yield http.post(`/assistants`, newAssistant);
        yield put(assistantActions.addAssistantSuccess(res.data?.msg));
        yield put(assistantActions.fetchAssistants());
        successMessage('Assistant added!');

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
        yield put(assistantActions.updateAssistantSuccess(res.data?.msg));
        yield put(assistantActions.fetchAssistants());
        successMessage('Assistant updated!');
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
        loadingMessage('Updating Script', 0);
        const res = yield http.put(`/assistant/${assistant.ID}/flow`, {flow: flow.parse(assistant.Flow)});
        yield put(assistantActions.updateFlowSuccess(assistant, res.data?.msg));
        successMessage('Script updated!');
    } catch (error) {
        console.error(error);
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

function* uploadLogo({assistantID, file}) {
    const defaultMsg = "Can't upload logo";
    try {
        loadingMessage('Uploading logo', 0);
        const res = yield http.post(`/assistant/${assistantID}/logo`, file);
        destroyMessage();
        successMessage(res.data?.msg || defaultMsg);
        yield put(assistantActions.fetchAssistants());
        yield put(assistantActions.uploadLogoSuccess(new Date().getTime()));
    } catch (error) {
        let data = error.response?.data;
        errorMessage(data.msg || defaultMsg);
        yield put(assistantActions.uploadLogoFailure(data.msg || defaultMsg));
        if (!data.msg) errorHandler(error)
    }
}

function* deleteLogo({assistantID}) {
    const defaultMsg = "Can't delete logo";
    try {
        loadingMessage('Deleting logo', 0);
        const res = yield http.delete(`/assistant/${assistantID}/logo`);
        destroyMessage();
        successMessage(res.data?.msg || defaultMsg);
        yield put(assistantActions.fetchAssistants());
        yield put(assistantActions.deleteLogoSuccess(new Date().getTime()));
    } catch (error) {
        let data = error.response?.data;
        errorMessage(data.msg || defaultMsg);
        yield put(assistantActions.deleteLogoFailure(data.msg || defaultMsg));
        if (!data.msg) errorHandler(error)
    }
}


function* watchDeleteLogo() {
    yield takeEvery(actionTypes.DELETE_LOGO_REQUEST, deleteLogo)
}


function* watchUploadLogo() {
    yield takeEvery(actionTypes.UPLOAD_LOGO_REQUEST, uploadLogo)
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
        watchUploadLogo(),
        watchDeleteLogo()
    ])
}
