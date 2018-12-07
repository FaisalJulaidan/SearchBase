import * as actionTypes from './actionTypes';


const fetchFlowRequest = (ID) => {
    return {
        type: actionTypes.FETCH_FLOW_REQUEST,
        ID
    };
};

const fetchFlowSuccess = (args) => {
    return {
        type: actionTypes.FETCH_FLOW_SUCCESS,
        ...args
    };
};

const fetchFlowFailure = (error) => {
    return {
        type: actionTypes.FETCH_FLOW_FAILURE,
        error
    };
};

//////////////////////////////////////////

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
    deleteGroupFailure
};