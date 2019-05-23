import * as actionTypes from './actionTypes';


const fetchConversations = (assistantID) => {
    return {
        type: actionTypes.FETCH_CONVERSATIONS_REQUEST,
        assistantID
    };
};

const fetchConversationsSuccess = (conversations) => {
    return {
        type: actionTypes.FETCH_CONVERSATIONS_SUCCESS,
        conversations
    };
};

const fetchConversationsFailure = (error) => {
    return {
        type: actionTypes.FETCH_CONVERSATIONS_FAILURE,
        error
    };
};

const deleteConversation = (conversationID, assistantID) => {
    return {
        type: actionTypes.DELETE_CONVERSATIONS_REQUEST,
        conversationID,
        assistantID
    };
};

const deleteConversationSuccess = (conversationID) => {
    return {
        type: actionTypes.DELETE_CONVERSATIONS_SUCCESS,
        conversationID
    };
};

const deleteConversationFailure = (error) => {
    return {
        type: actionTypes.DELETE_CONVERSATIONS_FAILURE,
        error
    };
};


const clearAllConversations = (assistantID) => {
    return {
        type: actionTypes.CLEAR_ALL_CONVERSATIONS_REQUEST,
        assistantID
    };
};

const clearAllConversationsSuccess = () => {
    return {
        type: actionTypes.CLEAR_ALL_CONVERSATIONS_SUCCESS,
    };
};

const clearAllConversationsFailure = (error) => {
    return {
        type: actionTypes.CLEAR_ALL_CONVERSATIONS_FAILURE,
        error
    };
};


export const conversationActions = {
    fetchConversations,
    fetchConversationsSuccess,
    fetchConversationsFailure,

    deleteConversation,
    deleteConversationSuccess,
    deleteConversationFailure,

    clearAllConversations,
    clearAllConversationsSuccess,
    clearAllConversationsFailure
};