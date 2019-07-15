import * as actionTypes from './actions';

const initialState = {
    isBotTyping: false
};

const reducer = (state=initialState, action) => {
    switch (action.type) {
        case actionTypes.UPDATE_IS_BOT_TYPING:
            return {
                ...state,
                isBotTyping: action.payload.value
            };
        default:
            return state;
    }
};

export default reducer;