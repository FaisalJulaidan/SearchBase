import {all, put, takeEvery, select} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {flowActions} from "../actions/flow.actions";
import {http} from "../../helpers";
import {alertError, alertSuccess, destroyMessage, loadingMessage} from "../../helpers/alert";


function* updateFlow({assistant}) {
    try {
        loadingMessage('Updating Block');
        const res = yield http.put(`/assistant/${assistant.id}/flow`, {flow: assistant.Flow});
        yield destroyMessage();
        yield alertSuccess('Block Updated', res.data.msg);

        yield put(flowActions.editBlockSuccess('done'));
        return yield put(flowActions.fetchFlowRequest(assistantID));
    } catch (error) {
        console.log(error);
        yield put(flowActions.editBlockFailure(error.response.data));
        return yield alertError('Error', "Sorry, we could not update the block");
    }
}

function* watchUpdateFlow() {
    yield takeEvery(actionTypes.UPDATE_FLOW_REQUEST, updateFlow)
}


export function* flowSaga() {
    yield all([watchUpdateFlow(),])
}