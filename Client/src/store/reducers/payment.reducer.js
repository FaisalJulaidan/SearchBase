import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {sessionID: null, isLoading: false, errorMsg: null};

export const payment = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.GENERATE_CHECKOUT_SESSION_REQUEST:
            return updateObject(state, {
                isLoading: true,
                sessionID: null,
                errorMsg: null,
            });
        case actionTypes.GENERATE_CHECKOUT_SESSION_SUCCESS:
            return updateObject(state, {
                isLoading: false,
                sessionID: action.sessionID,
                errorMsg: null
            });
        case actionTypes.GENERATE_CHECKOUT_SESSION_FAILURE:
            return updateObject(state, {
                isLoading: false,
                sessionID: null,
                errorMsg: action.error
            });
        default:
            return state
    }
};
