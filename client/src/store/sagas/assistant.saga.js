import {delay} from 'redux-saga'
import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {assistantActions, authActions} from "../actions";
import {http} from "../../helpers";

function* fetchAssistants() {
    yield delay(1000);
    try {
        const res = yield http.get(`admin/assistants`);
        return yield put(assistantActions.fetchAssistantsSuccess(res.data.data))
    } catch (error) {
        console.log(error);

        yield localStorage.removeItem('user');
        yield put(authActions.logout());
        return yield put(assistantActions.fetchAssistantsFailure(error.response.data));
    }

}

function* watchFetchAssistants() {
    yield takeEvery(actionTypes.FETCH_ASSISTANTS_REQUEST, fetchAssistants)
}


export function* assistantSaga() {
    yield all([
        watchFetchAssistants()
    ])
}