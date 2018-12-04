import {delay} from 'redux-saga'
import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {flowActions} from "../actions/flow.actions";
import {http} from "../../helpers";

function* fetchFlow() {
    yield delay(1000);

    try {
        // const res = yield http.get(`admin/assistants`);
        console.log('fetch flow is requested');
        return yield put(flowActions.fetchFlowSuccess())
    } catch (error) {
        console.log(error);
        return yield put(flowActions.fetchFlowFailure(error.response.data));
    }

}

function* watchFetchFlow() {
    yield takeEvery(actionTypes.FETCH_FLOW_REQUEST, fetchFlow)
}


export function* flowSaga() {
    yield all([
        watchFetchFlow()
    ])
}