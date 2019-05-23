import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {conversations: [], isLoading: false, errorMsg: null};

export const conversation = (state = initialState, action) => {
    switch (action.type) {
        // Fetching chatbot conversation
        case actionTypes.FETCH_CONVERSATIONS_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.FETCH_CONVERSATIONS_SUCCESS:
            return updateObject(state, {
                conversations: action.conversations,
                isLoading: false
            });
        case actionTypes.FETCH_CONVERSATIONS_FAILURE:
            return updateObject(state, {
                conversations: [],
                isLoading: false,
                errorMsg: action.error
            });

        // Delete chatbot conversation
        case actionTypes.DELETE_CONVERSATIONS_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isDeletingConversation: true
            });
        case actionTypes.DELETE_CONVERSATIONS_SUCCESS:

            const conversationsCopy = {...state.conversations,
                conversationsList: state.conversations.conversationsList.filter(conversation => conversation.ID !== action.conversationID)};

            return updateObject(state, {
                isDeletingConversation: false,
                conversations: conversationsCopy,
                errorMsg: null,
            });
        case actionTypes.DELETE_CONVERSATIONS_FAILURE:
            return updateObject(state, {
                isDeletingConversation: false,
                errorMsg: action.error
            });


        //Clearing all chatbot conversation
        case actionTypes.CLEAR_ALL_CONVERSATIONS_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isClearingAll: true
            });
        case actionTypes.CLEAR_ALL_CONVERSATIONS_SUCCESS:
            return updateObject(state, {
                isClearingAll: false,
                conversations: [],
                errorMsg: null,
            });
        case actionTypes.CLEAR_ALL_CONVERSATIONS_FAILURE:
            return updateObject(state, {
                isClearingAll: false,
                errorMsg: action.error
            });
        default:
            return state
    }
};