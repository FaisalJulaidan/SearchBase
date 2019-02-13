import {all, put, takeEvery} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {flowActions} from "../actions/flow.actions";
import {http} from "../../helpers";
import {alertError, alertSuccess, destroyMessage, loadingMessage} from "../../helpers/alert";

function* fetchFlow({assistantID}) {
    try {
        const res = yield http.get(`/assistant/${assistantID}/flow`);
        return yield put(flowActions.fetchFlowSuccess(res.data.data))
    } catch (error) {
        console.log(error);
        yield put(flowActions.fetchFlowFailure(error.response.data));
        return yield alertError('Error', "Sorry, we could not retrieve the flow");

    }

}

function* watchFetchFlow() {
    yield takeEvery(actionTypes.FETCH_FLOW_REQUEST, fetchFlow)
}

// Groups
function* addGroup({assistantID, newGroup}) {
    try {
        loadingMessage('Adding Group');
        const res = yield http.post(`/assistant/${assistantID}/flow/group`, newGroup);
        yield put(flowActions.fetchFlowRequest(assistantID));
        yield destroyMessage();
        return yield alertSuccess('Group Added', res.data.msg);

    } catch (error) {
        console.log(error);
        return yield put(flowActions.addGroupFailure(error.response.data));
    }
}

function* editGroup({assistantID, editedGroup}) {
    try {
        loadingMessage('Updating Group');
        const res = yield http.put(`/assistant/${assistantID}/flow/group`, editedGroup);
        yield put(flowActions.editGroupSuccess(res.data.msg));
        yield destroyMessage();
        yield alertSuccess('Group Updated', res.data.msg);
        return yield put(flowActions.fetchFlowRequest(assistantID))
    } catch (error) {
        console.log(error);
        yield destroyMessage();
        yield put(flowActions.editGroupFailure(error.response.data));
        return yield alertError('Error', "Sorry, we could not update the group.");

    }
}

function* deleteGroup({assistantID, deletedGroup}) {
    try {
        loadingMessage('Deleting Group');
        const res = yield http.delete(`/assistant/${assistantID}/flow/group`, {data: {id: deletedGroup.id}});
        yield put(flowActions.deleteGroupSuccess(res.data.msg, deletedGroup.id));
        yield destroyMessage();
        return yield alertSuccess('Group Deleted', res.data.msg);
    } catch (error) {
        console.log(error);
        yield destroyMessage();
        yield put(flowActions.deleteGroupFailure(error.response.data));
        return yield alertError('Error', "Sorry, we could not remove the group.");

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
        loadingMessage('Adding Block');
        const res = yield http.post(`/assistant/flow/group/${groupID}/block`, newBlock);

        yield destroyMessage();
        yield alertSuccess('Block Added', res.data.msg);
        yield put(flowActions.addBlockSuccess(res.data.msg));

        return yield put(flowActions.fetchFlowRequest(assistantID))
    } catch (error) {
        console.log(error);
        yield put(flowActions.addBlockFailure(error.response.data));
        return yield alertError('Error', "Sorry, we could not create the block");
    }
}

function* editBlock({edittedBlock, assistantID, currentBlocks}) {
    try {
        loadingMessage('Updating Block');
        let currentUpdatedGroup = [];
        edittedBlock = edittedBlock.block;
        currentBlocks.map(block =>
            block.ID === edittedBlock.ID ? currentUpdatedGroup.push(edittedBlock) : currentUpdatedGroup.push(block)
        );
        const res = yield http.put(`/assistant/${assistantID}/flow`, {blocks: currentUpdatedGroup});
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

function* deleteBlock({deletedBlock, assistantID, groupID}) {
    try {
        loadingMessage('Deleting Block');
        const res = yield http.delete(`/assistant/flow/group/${groupID}/block`, {data: {id: deletedBlock.ID}});
        yield put(flowActions.deleteBlockSuccess(res.data.msg));
        yield destroyMessage();
        yield alertSuccess('Block Deleted', res.data.msg);
        return yield put(flowActions.fetchFlowRequest(assistantID))
    } catch (error) {
        console.log(error);
        yield put(flowActions.deleteBlockFailure(error.response.data));
        return yield alertError('Error', "Sorry, we could not delete the block");
    }
}

function* updateBlocksOrder({newBlocksOrder, assistantID}) {
    try {
        loadingMessage('Updating Blocks Order');
        const res = yield http.put(`/assistant/${assistantID}/flow`, {blocks: newBlocksOrder});
        yield put(flowActions.updateBlocksOrderSuccess(res.data.msg));
        yield destroyMessage();
        return yield alertSuccess('Order Updated', res.data.msg);
    } catch (error) {
        console.log(error);
        yield destroyMessage();
        yield alertError('Error in Block Delete', error.message);
        yield put(flowActions.updateBlocksOrderFailure(error.response.data));
        return yield alertError('Error', "Sorry, we could not update the blocks order");
    }
}

function* watchAddBlock() {
    yield takeEvery(actionTypes.ADD_BLOCK_REQUEST, addBlock)
}

function* watchEditBlock() {
    yield takeEvery(actionTypes.EDIT_BLOCK_REQUEST, editBlock)
}

function* watchDeleteBlock() {
    yield takeEvery(actionTypes.DELETE_BLOCK_REQUEST, deleteBlock)
}

function* watchUpdateBlocksOrder() {
    yield takeEvery(actionTypes.UPDATE_BLOCKS_ORDER_REQUEST, updateBlocksOrder)
}

// Data Category (For Future)
function* addDataCategory({name}) {
    try {

    } catch (error) {

    }
}


export function* flowSaga() {
    yield all([
        watchFetchFlow(),

        watchAddGroup(),
        watchEditGroup(),
        watchDeleteGroup(),

        watchAddBlock(),
        watchEditBlock(),
        watchDeleteBlock(),
        watchUpdateBlocksOrder()
    ])
}