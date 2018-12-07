import {delay} from 'redux-saga'
import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {flowActions} from "../actions/flow.actions";
import {http} from "../../helpers";

function* fetchFlow(action) {
    yield delay(1000);

    try {
        const res = yield http.get(`/assistant/${action.ID}/flow`);

        return yield put(flowActions.fetchFlowSuccess(res.data.data))
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