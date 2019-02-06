import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {assistantList: [], isLoading: false, errorMsg: null};

export const assistant = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.FETCH_ASSISTANTS_REQUEST:
            return updateObject(state, {
                assistantList: [],
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.FETCH_ASSISTANTS_SUCCESS:
            return updateObject(state, {
                assistantList: action.assistantList,
                isLoading: false
            });
        case actionTypes.FETCH_ASSISTANTS_FAILURE:
            return updateObject(state, {
                assistantList: [],
                isLoading: false,
                errorMsg: action.error.msg
            });

        // Add
        case actionTypes.ADD_ASSISTANT_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isAdding: true
            });
        case actionTypes.ADD_ASSISTANT_SUCCESS:
            return updateObject(state, {
                successMsg: action.successMsg,
                isAdding: false
            });
        case actionTypes.ADD_ASSISTANT_FAILURE:
            return updateObject(state, {
                isAdding: false,
                errorMsg: action.error.msg
            });

        // Update
        case actionTypes.UPDATE_ASSISTANT_REQUEST:
            return updateObject(state, {
                successMsg: null,
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.UPDATE_ASSISTANT_SUCCESS:
            return updateObject(state, {
                successMsg: action.successMsg,
                isLoading: false
            });
        case actionTypes.UPDATE_ASSISTANT_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error.msg
            });

        // Delete
        case actionTypes.DELETE_ASSISTANT_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isDeleting: true
            });
        case actionTypes.DELETE_ASSISTANT_SUCCESS:

            let assistantList = [...state.assistantList];
            const assistantToDeleteIndex =  assistantList
                .findIndex(assistant => assistant.id === action.assistantID);
            assistantList.splice(assistantToDeleteIndex, 1);

            return updateObject(state, {
                successMsg: action.successMsg,
                isDeleting: false,
                assistantList
            });
        case actionTypes.DELETE_ASSISTANT_FAILURE:
            return updateObject(state, {
                isDeleting: false,
                errorMsg: action.error.msg
            });


        case actionTypes.CHANGE_ASSISTANT_STATUS_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isChanging: true
            });
        case actionTypes.CHANGE_ASSISTANT_STATUS_SUCCESS:

            return updateObject(state, {
                successMsg: action.successMsg,
                isChanging: false
            });
        case actionTypes.CHANGE_ASSISTANT_STATUS_FAILURE:
            return updateObject(state, {
                isChanging: false,
                errorMsg: action.error.msg
            });

        default:
            return state
    }
};