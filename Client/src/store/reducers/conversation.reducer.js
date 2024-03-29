import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {conversations: [], isLoading: false, errorMsg: null};

export const conversation = (state = initialState, action) => {
    switch (action.type) {
        // Fetching chatbot conversation
        case actionTypes.FETCH_CONVERSATIONS_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isLoading: true,
                conversations: []
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


        // Updating conversation status
        case actionTypes.UPDATE_CONVERSATION_STATUS_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isUpdatingStatus: true
            });
        case actionTypes.UPDATE_CONVERSATION_STATUS_SUCCESS:
            const conversationsCopy2 = {...state.conversations,
                conversationsList: state.conversations.conversationsList
                    .map(c => c.ID === action.conversationID ? {...c,ApplicationStatus: action.newStatus}: c)};

            return updateObject(state, {
                isUpdatingStatus: false,
                conversations: conversationsCopy2,
                errorMsg: null,
            });
        case actionTypes.UPDATE_CONVERSATION_STATUS_FAILURE:
            return updateObject(state, {
                isUpdatingStatus: false,
                errorMsg: action.errorMsg
            });

        default:
            return state
    }
};
