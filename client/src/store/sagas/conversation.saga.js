import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {conversationActions} from "../actions";
import {http, successMessage, errorMessage, loadingMessage} from "helpers";

function* fetchConversations({assistantID}) {
    try {
        const res = yield http.get(`/assistant/${assistantID}/conversations`);
        return yield put(conversationActions.fetchConversationsSuccess(res.data.data))
    } catch (error) {
        console.log(error);
        const msg = "Couldn't load conversation";
        yield put(conversationActions.fetchConversationsFailure(msg));
        errorMessage(msg);
    }
}

function* watchFetchConversations() {
    yield takeEvery(actionTypes.FETCH_CONVERSATIONS_REQUEST, fetchConversations)
}

function* deleteConversation({conversationID, assistantID}) {
    try {
        loadingMessage('Removing conversation...', 0);
        const res = yield http.delete(`/assistant/${assistantID}/conversation/${conversationID}`);
        yield put(conversationActions.deleteConversationSuccess(conversationID));
        successMessage('Conversation removed');
    } catch (error) {
        console.log(error);
        const msg = "Couldn't delete conversation";
        yield put(conversationActions.deleteConversationFailure(msg));
        errorMessage(msg);
    }
}

function* watchDeleteConversation() {
    yield takeEvery(actionTypes.DELETE_CONVERSATIONS_REQUEST, deleteConversation)
}


function* clearAllConversations({assistantID}) {
    try {
        loadingMessage('Removing all conversation...', 0);
        const res = yield http.delete(`/assistant/${assistantID}/conversation`);
        yield put(conversationActions.clearAllConversationsSuccess());
        successMessage('All conversation cleared');
    } catch (error) {
        console.log(error);
        const msg = "Couldn't clear all conversation";
        yield put(conversationActions.clearAllConversationsFailure(msg));
        errorMessage(msg);
    }
}

function* watchClearAllConversations() {
    yield takeEvery(actionTypes.CLEAR_ALL_CONVERSATIONS_REQUEST, clearAllConversations)
}

function* updateConversationStatus({newStatus, conversationID, assistantID}) {
    try {
        loadingMessage('Updating application status...', 0);
        const res = yield http.put(`/assistant/${assistantID}/conversation/${conversationID}/status`,
                                   {newStatus: newStatus});
        yield put(conversationActions.updateConversationStatusSuccess(conversationID, newStatus));
        successMessage('Application status updated');
    } catch (error) {
        console.log(error);
        const msg = "Couldn't update application status";
        yield put(conversationActions.updateConversationStatusFailure(msg));
        errorMessage(msg);
    }
}

function* watchUpdateConversationStatus() {
    yield takeEvery(actionTypes.UPDATE_CONVERSATION_STATUS_REQUEST, updateConversationStatus)
}


export function* conversationSaga() {
    yield all([
        watchFetchConversations(),
        watchDeleteConversation(),
        watchClearAllConversations(),
        watchUpdateConversationStatus(),
    ])
}