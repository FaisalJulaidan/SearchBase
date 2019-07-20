import * as actionTypes from '../constants/actionTypes';

let messageID = 0;

export const addBotMessage = (text, messageType, block) => ({
    type: actionTypes.ADD_MESSAGE,
    payload: {
        type: messageType,
        text,
        block: block,
        sender: 'BOT',
        index: messageID++
    }
});

export const addUserMessage = (text, messageType, blockRef, content = {}) => ({
    type: actionTypes.ADD_MESSAGE,
    payload: {
        type: messageType,
        blockRef,
        text,
        sender: 'USER',
        index: messageID++,
        content
    }
});

export const rewindToMessage = (index) => ({
    type: actionTypes.REWIND_TO_INDEX,
    index
});

export const resetMessage = () => ({
    type: actionTypes.RESET_MESSAGE
});

export const initChatbot = (assistant, blocks, status = {}) => ({
    type: actionTypes.INIT_CHATBOT,
    assistant,
    blocks,
    status: {
        loading: false,
        ...status
    }
});


export const setChatbotStatus = (status = {}) => ({
    type: actionTypes.SET_CHATBOT_STATUS,
    status: {
        ...status
    }
});

export const setChatbotAnimation = (animation = {}) => ({
    type: actionTypes.SET_CHATBOT_ANIMATION,
    status: {
        open: true,
    },
    animation: {
        ...animation
    }
});

export const resetChatbot = () => ({
    type: actionTypes.RESET_CHATBOT,
    status: {
        open: true,
        loading: false
    },
    animation: {open: true}
});

