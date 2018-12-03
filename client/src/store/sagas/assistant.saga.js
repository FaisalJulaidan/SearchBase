import {delay} from 'redux-saga'
import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {assistantActions} from "../actions/assistant.action";
import {http} from "../../helpers";

function* fetchAssistants() {
    yield delay(1000);
    try {
        const res = yield http.get(`api/admin/assistants`);
        return yield put(assistantActions.fetchAssistantsSuccess(res.data.data))
    } catch (e) {
        console.log(e);
        return yield put(assistantActions.fetchAssistantsFailure());
    }

}

function* watchFetchAssistants() {
    yield takeEvery(actionTypes.FETCH_ASSISTANTS, fetchAssistants)
}


export function* assistantSaga() {
    yield all([
        watchFetchAssistants()
    ])
}