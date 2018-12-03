import {delay} from 'redux-saga'
import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {assistantActions} from "../actions/assistant.action";
import {http} from "../../helpers";

function* fetchAssistants() {
    yield delay(1000);
    try {
        const res = yield http.get(`api/admin/assistants`);
        console.log(res)
        return yield put(assistantActions.fetchAssistantsSuccess([1, 2, 3, 4, 5, 6]));
    } catch (e) {
        console.log(e);
        return yield put(assistantActions.fetchAssistantsFailure());
    }

}

function* watchfetchAssistants() {
    yield takeEvery(actionTypes.FETCH_ASSISTANTS, fetchAssistants)
}


export function* assistantSaga() {
    yield all([
        watchfetchAssistants()
    ])
}