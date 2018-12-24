import * as actionTypes from './actionTypes';


const fetchFlowRequest = (assistantID) => {
    return {
        type: actionTypes.FETCH_FLOW_REQUEST,
        assistantID
    };
};

const fetchFlowSuccess = (args) => {
    return {
        type: actionTypes.FETCH_FLOW_SUCCESS,
        blockGroups: args.blockGroups
    };
};

const fetchFlowFailure = (error) => {
    return {
        type: actionTypes.FETCH_FLOW_FAILURE,
        error
    };
};

// Groups Actions
const addGroupRequest = (values) => {
    return {
        type: actionTypes.ADD_GROUP_REQUEST,
        ID: values.ID,
        newGroup: values.newGroup
    };
};

const addGroupSuccess = (msg) => {
    return {
        type: actionTypes.ADD_GROUP_SUCCESS,
        msg
    };
};

const addGroupFailure = (error) => {
    return {
        type: actionTypes.ADD_GROUP_FAILURE,
        error
    };
};

//////////////////////////////////////////

const editGroupRequest = (values) => {
    return {
        type: actionTypes.EDIT_GROUP_REQUEST,
        ID: values.ID,
        editedGroup: values.editedGroup
    };
};

const editGroupSuccess = (msg) => {
    return {
        type: actionTypes.EDIT_GROUP_SUCCESS,
        msg
    };
};

const editGroupFailure = (error) => {
    return {
        type: actionTypes.EDIT_GROUP_FAILURE,
        error
    };
};

//////////////////////////////////////////

const deleteGroupRequest = (values) => {
    return {
        type: actionTypes.DELETE_GROUP_REQUEST,
        ID: values.ID,
        deletedGroup: values.deletedGroup
    };
};

const deleteGroupSuccess = (msg) => {
    return {
        type: actionTypes.DELETE_GROUP_SUCCESS,
        msg
    };
};

const deleteGroupFailure = (error) => {
    return {
        type: actionTypes.DELETE_GROUP_FAILURE,
        error
    };
};

//////////////////////////////////////////
// ADD Blocks Actions
const addBlockRequest = ({newBlock, assistantID, groupID}) => {
    return {
        type: actionTypes.ADD_BLOCK_REQUEST,
        newBlock,
        assistantID,
        groupID
    };
};

const addBlockSuccess = (msg) => {
    return {
        type: actionTypes.ADD_BLOCK_SUCCESS,
        msg
    };
};

const addBlockFailure = (error) => {
    return {
        type: actionTypes.ADD_BLOCK_FAILURE,
        error
    };
};
//////////////////////////////////////////
// EDIT Blocks Actions
const editBlockRequest = ({edittedBlock, assistantID, groupID}) => {
    return {
        type: actionTypes.EDIT_BLOCK_REQUEST,
        edittedBlock,
        assistantID,
        groupID
    };
};

const editBlockSuccess = (msg) => {
    return {
        type: actionTypes.EDIT_BLOCK_SUCCESS,
        msg
    };
};

const editBlockFailure = (error) => {
    return {
        type: actionTypes.EDIT_BLOCK_FAILURE,
        error
    };
};
//////////////////////////////////////////

export const flowActions = {
    fetchFlowRequest,
    fetchFlowSuccess,
    fetchFlowFailure,

    addGroupRequest,
    addGroupSuccess,
    addGroupFailure,

    editGroupRequest,
    editGroupSuccess,
    editGroupFailure,

    deleteGroupRequest,
    deleteGroupSuccess,
    deleteGroupFailure,

    addBlockRequest,
    addBlockSuccess,
    addBlockFailure,

    editBlockRequest,
    editBlockSuccess,
    editBlockFailure
};