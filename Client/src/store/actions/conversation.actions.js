import * as actionTypes from './actionTypes';


const fetchConversations = (assistantID) => ({
    type: actionTypes.FETCH_CONVERSATIONS_REQUEST,
    meta: {thunk: true},
    assistantID
});

const fetchConversationsSuccess = (conversations) => ({
    type: actionTypes.FETCH_CONVERSATIONS_SUCCESS,
    conversations
});

const fetchConversationsFailure = (error) => ({
    type: actionTypes.FETCH_CONVERSATIONS_FAILURE,
    error
});

const deleteConversation = (conversationID, assistantID) => ({
    type: actionTypes.DELETE_CONVERSATIONS_REQUEST,
    conversationID,
    assistantID
});

const deleteConversationSuccess = (conversationID) => ({
    type: actionTypes.DELETE_CONVERSATIONS_SUCCESS,
    conversationID
});

const deleteConversationFailure = (error) => ({
    type: actionTypes.DELETE_CONVERSATIONS_FAILURE,
    error
});


const clearAllConversations = (assistantID) => ({
    type: actionTypes.CLEAR_ALL_CONVERSATIONS_REQUEST,
    assistantID
});

const clearAllConversationsSuccess = () => ({
    type: actionTypes.CLEAR_ALL_CONVERSATIONS_SUCCESS,
});

const clearAllConversationsFailure = (error) => ({
    type: actionTypes.CLEAR_ALL_CONVERSATIONS_FAILURE,
    error
});


const updateConversationStatus = (newStatus, conversationID, assistantID) => ({
    type: actionTypes.UPDATE_CONVERSATION_STATUS_REQUEST,
    newStatus,
    conversationID,
    assistantID
});

const updateConversationStatusSuccess = (conversationID, newStatus) => ({
    type: actionTypes.UPDATE_CONVERSATION_STATUS_SUCCESS,
    conversationID,
    newStatus
});

const updateConversationStatusFailure = (errorMsg) => ({
    type: actionTypes.UPDATE_CONVERSATION_STATUS_FAILURE,
    errorMsg,
});


export const conversationActions = {
    fetchConversations,
    fetchConversationsSuccess,
    fetchConversationsFailure,

    deleteConversation,
    deleteConversationSuccess,
    deleteConversationFailure,

    clearAllConversations,
    clearAllConversationsSuccess,
    clearAllConversationsFailure,

    updateConversationStatus,
    updateConversationStatusSuccess,
    updateConversationStatusFailure,
};
