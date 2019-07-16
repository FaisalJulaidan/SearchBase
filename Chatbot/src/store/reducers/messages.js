const initialState = {
    messageList: []
};

const messages = (state = initialState, action) => {
    switch (action.type) {
        case 'ADD_MESSAGE':
            return {
                ...state,
                messageList: state.messageList.concat({ ...action.payload })
            };
        case 'REMOVE_MESSAGE':
            return { ...state };
        case 'REWIND_TO_INDEX':
            return {...state, messageList: state.messageList.filter(msg => msg.index <= action.index)}
        case 'RESET_MESSAGE':
            return {
                ...state,
                messageList: []
            };
        default:
            return state;
    }
};

export default messages;


// export const addBotMessage = (block, text, messageType) => ({
//     type: actionTypes.ADD_MESSAGE,
//     messageType,
//     text,
//     block: block,
//     sender: 'BOT',
//     index: messageID++
// });

// export const addUserMessage = (text, messageType, blockRef) => ({
//     type: actionTypes.ADD_MESSAGE,
//     messageType,
//     blockRef,
//     text,
//     sender: 'USER',
//     index: messageID++
// });
