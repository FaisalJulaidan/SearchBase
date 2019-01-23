import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {chatbotSessionsActions} from "../actions";
import {http, alertSuccess, alertError} from "../../helpers";

function* fetchChatbotSessions({assistantID}) {
    try {
        const res = yield http.get(`/assistant/${assistantID}/chatbotSessions`);
        return yield put(chatbotSessionsActions.fetchChatbotSessionsSuccess(res.data.data))
    } catch (error) {
        console.log(error);
        return yield put(chatbotSessionsActions.fetchChatbotSessionsFailure(error));
    }
}

function* watchFetchChatbotSessions() {
    yield takeEvery(actionTypes.FETCH_CHATBOT_SESSIONS_REQUEST, fetchChatbotSessions)
}

function* clearAllChatbotSessions({assistantID}) {
    try {
        const res = yield http.delete(`/assistant/${assistantID}/chatbotSessions`);
        yield put(chatbotSessionsActions.clearAllChatbotSessionsSuccess());
        return yield alertSuccess('Cleared Successfully', res.data.msg)
    } catch (error) {
        console.log(error);
        yield put(chatbotSessionsActions.clearAllChatbotSessionsFailure(error));
        return yield alertError('Error', "Sorry, we could'nt clear all the records!");

    }
}

function* watchClearAllChatbotSessions() {
    yield takeEvery(actionTypes.CLEAR_ALL_CHATBOT_SESSIONS_REQUEST, clearAllChatbotSessions)
}


export function* chatbotSessions() {
    yield all([
        watchFetchChatbotSessions(),
        watchClearAllChatbotSessions(),
    ])
}