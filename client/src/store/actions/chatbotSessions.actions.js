import * as actionTypes from './actionTypes';


const fetchChatbotSessions = (assistantID) => {
    return {
        type: actionTypes.FETCH_CHATBOT_SESSIONS_REQUEST,
        assistantID
    };
};

const fetchChatbotSessionsSuccess = (chatbotSessions) => {
    return {
        type: actionTypes.FETCH_CHATBOT_SESSIONS_SUCCESS,
        chatbotSessions
    };
};

const fetchChatbotSessionsFailure = (error) => {
    return {
        type: actionTypes.FETCH_CHATBOT_SESSIONS_FAILURE,
        error
    };
};


const clearAllChatbotSessions = (assistantID) => {
    return {
        type: actionTypes.CLEAR_ALL_CHATBOT_SESSIONS_REQUEST,
        assistantID
    };
};

const clearAllChatbotSessionsSuccess = () => {
    return {
        type: actionTypes.CLEAR_ALL_CHATBOT_SESSIONS_SUCCESS,
    };
};

const clearAllChatbotSessionsFailure = (error) => {
    return {
        type: actionTypes.CLEAR_ALL_CHATBOT_SESSIONS_FAILURE,
        error
    };
};


export const chatbotSessionsActions = {
    fetchChatbotSessions,
    fetchChatbotSessionsSuccess,
    fetchChatbotSessionsFailure,

    clearAllChatbotSessions,
    clearAllChatbotSessionsSuccess,
    clearAllChatbotSessionsFailure
};