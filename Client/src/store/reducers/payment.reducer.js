import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {sessionID: null, isLoading: false, errorMsg: null};

export const payment = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.FETCH_ANALYTICS_REQUEST:
            return updateObject(state, {
                analytics: null,
                isLoading: true,
                errorMsg: null,
            });
        case actionTypes.FETCH_ANALYTICS_SUCCESS:
            return updateObject(state, {
                sessionID: action.sessionID,
                isLoading: false,
                errorMsg: null
            });
        case actionTypes.FETCH_ANALYTICS_FAILURE:
            return updateObject(state, {
                sessionID: null,
                isLoading: false,
                errorMsg: action.error
            });
        default:
            return state
    }
};
