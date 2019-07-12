const initialState = {
    status: {
        open: false,
        disabled: false,
        finished: false, 
        loading: true,
        thinking: false,
        fetching: false,
        started: false,
        curBlockID: null,
        curBlock: null,
        curAction: 'Init',
        waitingForUser: false,
        ref: null
    },
    animation: {
        inputOpen: false,
        open: false
    }
};

const chatbot = (state = initialState, action) => {
    switch (action.type) {
        case 'INIT_CHATBOT':
            const { assistant, blocks } = action;
            return {
                assistant,
                blocks,
                status: { ...state.status, ...action.status },
                animation: { ...state.animation }
            };
        case 'SET_CHATBOT_STATUS':
            return { ...state, status: { ...state.status, ...action.status } };
        case 'SET_CHATBOT_ANIMATION':
            return { ...state, animation: { ...state.animation, ...action.animation } };
        case 'RESET_CHATBOT':
            return {
                ...state, ...initialState,
                status: { ...initialState.status, ...action.status },
                animation: {...initialState.animation, ...action.animation}
            };
        default:
            return state;
    }
};
export default chatbot;
