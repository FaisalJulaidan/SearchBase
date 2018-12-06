import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {assistantActions, authActions} from "../actions";
import {http} from "../../helpers";

function* fetchAssistants() {
    try {
        const res = yield http.get(`/assistants`);
        return yield put(assistantActions.fetchAssistantsSuccess(res.data.data))
    } catch (error) {
        console.log(error);

        yield localStorage.removeItem('user');
        yield put(authActions.logout());
        return yield put(assistantActions.fetchAssistantsFailure(error.response.data));
    }

}

function* addAssistant(action) {
    console.log(action);
    try {
        const res = yield http.post(`/assistants`, action);
        return yield put(assistantActions.addAssistantSuccess(res.data.msg))
    } catch (error) {
        // console.log(error);
        //
        // yield localStorage.removeItem('user');
        // yield put(authActions.logout());
        // return yield put(assistantActions.fetchAssistantsFailure(error.response.data));
    }

}

function* watchFetchAssistants() {
    yield takeEvery(actionTypes.FETCH_ASSISTANTS_REQUEST, fetchAssistants)
}

function* watchAddAssistant() {
    yield takeEvery(actionTypes.ADD_ASSISTANT_REQUEST, addAssistant)
}


export function* assistantSaga() {
    yield all([
        watchFetchAssistants(),
        watchAddAssistant()
    ])
}