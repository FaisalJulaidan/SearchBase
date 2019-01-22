import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {isLoading: false, errorMsg: null, blockGroups: []};

export const flow = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.FETCH_FLOW_REQUEST:
            return updateObject(state, {
                isLoading: true
            });
        case actionTypes.FETCH_FLOW_SUCCESS:
            return updateObject(state, {
                isLoading: false,
                blockGroups: action.blockGroups
            });
        case actionTypes.FETCH_FLOW_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error.msg
            });

        // Groups
        case actionTypes.ADD_GROUP_REQUEST:
            return updateObject(state, {
                isAddingGroup: true
            });
        case actionTypes.ADD_GROUP_SUCCESS:
            return updateObject(state, {
                isAddingGroup: false,
                addSuccessMsg: action.msg
            });
        case actionTypes.ADD_GROUP_FAILURE:
            return updateObject(state, {
                isAddingGroup: false,
                errorMsg: action.error.msg
            });


        case actionTypes.EDIT_GROUP_REQUEST:
            return updateObject(state, {
                isEditingGroup: true
            });
        case actionTypes.EDIT_GROUP_SUCCESS:
            return updateObject(state, {
                isEditingGroup: false,
                editSuccessMsg: action.msg
            });
        case actionTypes.EDIT_GROUP_FAILURE:
            return updateObject(state, {
                isEditingGroup: false,
                errorMsg: action.error.msg
            });


        case actionTypes.DELETE_GROUP_REQUEST:
            return updateObject(state, {
                isDeletingGroup: true
            });
        case actionTypes.DELETE_GROUP_SUCCESS:
            let blockGroups = [...state.blockGroups];
            const groupToDeleteIndex =  blockGroups.findIndex(group => group.id === action.groupID);
            blockGroups.splice(groupToDeleteIndex, 1);

            return updateObject(state, {
                isDeletingGroup: false,
                deleteSuccessMsg: action.msg,
                blockGroups
            });
        case actionTypes.DELETE_GROUP_FAILURE:
            return updateObject(state, {
                isDeletingGroup: false,
                errorMsg: action.error.msg
            });


        // Blocks
        case actionTypes.ADD_BLOCK_REQUEST:
            return updateObject(state, {
                isAddingBlock: true
            });
        case actionTypes.ADD_BLOCK_SUCCESS:
            return updateObject(state, {
                isAddingBlock: false,
                successMsg: action.msg
            });
        case actionTypes.ADD_BLOCK_FAILURE:
            return updateObject(state, {
                isAddingBlock: false,
                errorMsg: action.error.msg
            });


        case actionTypes.DELETE_BLOCK_REQUEST:
            return updateObject(state, {
                isDeletingBlock: true
            });
        case actionTypes.DELETE_BLOCK_SUCCESS:
            return updateObject(state, {
                isDeletingBlock: false,
                deleteSuccessMsg: action.msg,
            });
        case actionTypes.DELETE_BLOCK_FAILURE:
            return updateObject(state, {
                isDeletingBlock: false,
                errorMsg: action.error.msg
            });


        default:
            return state
    }
};