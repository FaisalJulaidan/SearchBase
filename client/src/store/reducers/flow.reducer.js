import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {isLoading: false, errorMsg: null};

export const flow = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.FETCH_ASSISTANTS_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.FETCH_ASSISTANTS_SUCCESS:
            return updateObject(state, {
                isLoading: false
            });
        case actionTypes.FETCH_ASSISTANTS_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error.msg
            });
        default:
            return state
    }
};