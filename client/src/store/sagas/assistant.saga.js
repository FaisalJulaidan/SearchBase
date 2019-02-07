import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {assistantActions, authActions, flowActions} from "../actions";
import {http} from "../../helpers";
import {alertError, alertSuccess, destroyMessage, loadingMessage} from "../../helpers/alert";


function* fetchAssistants() {
    try {
        const res = yield http.get(`/assistants`);
        yield put(assistantActions.fetchAssistantsSuccess(res.data.data));
    } catch (error) {
        console.log(error);
        yield put(assistantActions.fetchAssistantsFailure(error.response.data));
        return yield alertError('Error', "Sorry, we could not fetch your assistants.");
    }

}

function* addAssistant({type, newAssistant}) {
    try {
        const res = yield http.post(`/assistants`, newAssistant);
        yield put(assistantActions.addAssistantSuccess(res.data.msg));
        yield put(assistantActions.fetchAssistants())
        return yield alertSuccess('Assistant Added', res.data.msg);

    } catch (error) {
        console.log(error);
        yield put(assistantActions.addAssistantFailure(error.response.data));
        return yield alertError('Error', "Sorry, we could not create the assistant.");
    }
}

function* updateAssistant({assistantID, updatedSettings}) {
    try {
        const res = yield http.put(`assistant/${assistantID}`, updatedSettings);
        yield put(assistantActions.updateAssistantSuccess(res.data.msg));
        yield put(assistantActions.fetchAssistants());
        return yield alertSuccess('Assistant Updated', res.data.msg);
    } catch (error) {
        console.log(error);
        yield put(assistantActions.updateAssistantFailure(error.response.data));
        return yield alertError('Error', "Sorry, we could not update the assistant.");

    }
}


function* deleteAssistant({assistantID}) {
    try {
        const res = yield http.delete(`/assistant/${assistantID}`);
        yield put(assistantActions.deleteAssistantSuccess(assistantID, res.data.msg));
        return yield alertSuccess('Assistant Deleted', res.data.msg);
    } catch (error) {
        console.log(error);
        yield put(assistantActions.deleteAssistantFailure(error.response.data));
        return yield alertError('Error', "Sorry, we could not remove the assistant.");
    }
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

    ])
}