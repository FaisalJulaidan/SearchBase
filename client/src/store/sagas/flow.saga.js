import {all, put, takeEvery} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {flowActions} from "../actions/flow.actions";
import {alertSuccess, http} from "../../helpers";

function* fetchFlow({assistantID}) {
    try {
        console.log(assistantID);
        const res = yield http.get(`/assistant/${assistantID}/flow`);
        return yield put(flowActions.fetchFlowSuccess(res.data.data))
    } catch (error) {
        console.log(error);
        return yield put(flowActions.fetchFlowFailure(error.response.data));
    }

}

function* watchFetchFlow() {
    yield takeEvery(actionTypes.FETCH_FLOW_REQUEST, fetchFlow)
}

// Groups
function* addGroup(action) {
    try {
        const res = yield http.post(`/assistant/${action.ID}/flow/group`, action.newGroup);
        yield put(flowActions.addGroupSuccess(res.data.msg));
        yield alertSuccess('title', 'success success yaaa!');
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


function* deleteGroup({type, assistantID, deletedGroup}) {
    try {
        console.log(deletedGroup)
        const res = yield http.delete(`/assistant/${assistantID}/flow/group`, {data: {id: deletedGroup.id}});
        yield put(flowActions.deleteGroupSuccess(res.data.msg));
        return yield put(flowActions.fetchFlowRequest(assistantID))
    } catch (error) {
        console.log(error);
        return yield put(flowActions.deleteGroupFailure(error.response.data));
    }
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

// Blocks
function* addBlock({newBlock, groupID, assistantID}) {
    try {
        console.log(newBlock)
        const res = yield http.post(`/assistant/flow/group/${groupID}/block`, newBlock);
        yield put(flowActions.addBlockSuccess(res.data.msg));
        return yield put(flowActions.fetchFlowRequest(assistantID))
    } catch (error) {
        console.log(error);
        return yield put(flowActions.addBlockFailure(error.response.data));
    }
}

function* editBlock({edittedBlock, groupID, assistantID}) {
    try {
        // prepair flow and add the editted block to the whole flow
        let res = yield http.get(`/assistant/${assistantID}/flow`);
        res.data.data.blockGroups.map((group, i) => {
            if (group.id === groupID)
                group.blocks.map((block, j) => {
                    if (block.id === edittedBlock.id)
                        res.data.data.blockGroups[i].blocks[j] = edittedBlock
                })
        });
        const allFlows = res.data.data.blockGroups.map((group) => group.blocks);
        const allFlow = {
            blocks: []
        };
        allFlows.map(eachFlow => eachFlow.map((block) => {
            block.groupID = groupID;
            allFlow.blocks.push(block)
        }));
        console.log(allFlow);
        res = yield http.put(`/assistant/${assistantID}/flow`, allFlow);


        // yield put(flowActions.addBlockSuccess(res.data.msg));
        console.log(res);
        // yield put(flowActions.editBlockSuccess(res.data.msg));
        yield put(flowActions.editBlockSuccess(''));
        return yield put(flowActions.fetchFlowRequest(assistantID))
    } catch (error) {
        console.log(error);
        return yield put(flowActions.editBlockFailure(error.response.data));
    }
}


function* watchAddBlock() {
    yield takeEvery(actionTypes.ADD_BLOCK_REQUEST, addBlock)
}

function* watchEditBlock() {
    yield takeEvery(actionTypes.EDIT_BLOCK_REQUEST, editBlock)
}

export function* flowSaga() {
    yield all([
        watchFetchFlow(),
        watchAddGroup(),
        watchEditGroup(),
        watchDeleteGroup(),
        watchAddBlock(),
        watchEditBlock(),
    ])
}