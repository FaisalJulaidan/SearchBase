import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {chatbotSessions: [], isLoading: false, errorMsg: null};

export const chatbotSessions = (state = initialState, action) => {
    switch (action.type) {
        // Fetching chatbot sessions
        case actionTypes.FETCH_CHATBOT_SESSIONS_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.FETCH_CHATBOT_SESSIONS_SUCCESS:
            return updateObject(state, {
                chatbotSessions: action.chatbotSessions,
                isLoading: false
            });
        case actionTypes.FETCH_CHATBOT_SESSIONS_FAILURE:
            return updateObject(state, {
                chatbotSessions: [],
                isLoading: false,
                errorMsg: action.error.msg
            });

        //Clearing all chatbot sessions
        case actionTypes.CLEAR_ALL_CHATBOT_SESSIONS_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isClearingAll: true
            });
        case actionTypes.CLEAR_ALL_CHATBOT_SESSIONS_SUCCESS:
            return updateObject(state, {
                isClearingAll: false,
                chatbotSessions: [],
                errorMsg: null,
            });
        case actionTypes.CLEAR_ALL_CHATBOT_SESSIONS_FAILURE:
            return updateObject(state, {
                isClearingAll: false,
                errorMsg: action.error.msg
            });
        default:
            return state
    }
};