import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {chatbotSessionsActions} from "../actions";
import {http, successMessage, errorMessage, loadingMessage} from "../../helpers";

function* fetchChatbotSessions({assistantID}) {
    try {
        const res = yield http.get(`/assistant/${assistantID}/chatbotSessions`);
        return yield put(chatbotSessionsActions.fetchChatbotSessionsSuccess(res.data.data))
    } catch (error) {
        console.log(error);
        const msg = "Couldn't load conversations";
        yield put(chatbotSessionsActions.fetchChatbotSessionsFailure(msg));
        errorMessage(msg);
    }
}

function* watchFetchChatbotSessions() {
    yield takeEvery(actionTypes.FETCH_CHATBOT_SESSIONS_REQUEST, fetchChatbotSessions)
}

function* deleteChatbotSession({sessionID, assistantID}) {
    try {
        loadingMessage('Removing conversation...', 0);
        const res = yield http.delete(`/assistant/${assistantID}/chatbotSessions/${sessionID}`);
        yield put(chatbotSessionsActions.deleteChatbotSessionSuccess(sessionID));
        successMessage('Session removed');
    } catch (error) {
        console.log(error);
        const msg = "Couldn't delete conversations";
        yield put(chatbotSessionsActions.deleteChatbotSessionFailure(msg));
        errorMessage(msg);
    }
}

function* watchDeleteChatbotSession() {
    yield takeEvery(actionTypes.DELETE_CHATBOT_SESSION_REQUEST, deleteChatbotSession)
}


function* clearAllChatbotSessions({assistantID}) {
    try {
        loadingMessage('Removing all sessions...', 0);
        const res = yield http.delete(`/assistant/${assistantID}/chatbotSessions`);
        yield put(chatbotSessionsActions.clearAllChatbotSessionsSuccess());
        successMessage('All sessions cleared');
    } catch (error) {
        console.log(error);
        const msg = "Couldn't clear all conversations";
        yield put(chatbotSessionsActions.clearAllChatbotSessionsFailure(msg));
        errorMessage(msg);
    }
}

function* watchClearAllChatbotSessions() {
    yield takeEvery(actionTypes.CLEAR_ALL_CHATBOT_SESSIONS_REQUEST, clearAllChatbotSessions)
}


export function* chatbotSessions() {
    yield all([
        watchFetchChatbotSessions(),
        watchDeleteChatbotSession(),
        watchClearAllChatbotSessions(),
    ])
}