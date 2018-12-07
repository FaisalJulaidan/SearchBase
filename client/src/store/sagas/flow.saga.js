import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {flowActions} from "../actions/flow.actions";
import {http} from "../../helpers";
import {delay} from "redux-saga";

function* fetchFlow(action) {
    try {
        const res = yield http.get(`/assistant/${action.ID}/flow`);
        return yield put(flowActions.fetchFlowSuccess(res.data.data))
    } catch (error) {
        console.log(error);
        return yield put(flowActions.fetchFlowFailure(error.response.data));
    }

}

function* addGroup(action) {
    try {
        const res = yield http.post(`/assistant/${action.ID}/flow/group`, action.newGroup);
        yield put(flowActions.addGroupSuccess(res.data.msg));
        return yield put(flowActions.fetchFlowRequest(action.ID))
    } catch (error) {
        console.log(error);
        return yield put(flowActions.addGroupFailure(error.response.data));
    }

}

function* editGroup(action) {
    try {
        const res = yield http.put(`/assistant/${action.ID}/flow/group`, action.editedGroup);
        yield put(flowActions.editGroupSuccess(res.data.msg));
        return yield put(flowActions.fetchFlowRequest(action.ID))
    } catch (error) {
        console.log(error);
        return yield put(flowActions.editGroupFailure(error.response.data));
    }
}

function* deleteGroup(action) {
    try {
        const res = yield http.delete(`/assistant/${action.ID}/flow/group`, action.deletedGroup);
        yield put(flowActions.deleteGroupSuccess(res.data.msg));
        return yield put(flowActions.fetchFlowRequest(action.ID))
    } catch (error) {
        console.log(error);
        return yield put(flowActions.deleteGroupFailure(error.response.data));
    }
}


function* watchFetchFlow() {
    yield takeEvery(actionTypes.FETCH_FLOW_REQUEST, fetchFlow)
}

function* watchAddGroup() {
    yield takeEvery(actionTypes.ADD_GROUP_REQUEST, addGroup)
}

function* watchEditGroup() {
    yield takeEvery(actionTypes.EDIT_GROUP_REQUEST, editGroup)
}

function* watchDeleteGroup() {
    yield takeEvery(actionTypes.DELETE_GROUP_REQUEST, deleteGroup)
}


export function* flowSaga() {
    yield all([
        watchFetchFlow(),
        watchAddGroup(),
        watchEditGroup(),
        watchDeleteGroup()
    ])
}