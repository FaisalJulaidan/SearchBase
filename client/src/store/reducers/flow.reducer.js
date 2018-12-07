import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {isLoading: false, errorMsg: null};

export const flow = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.FETCH_FLOW_REQUEST:
            return updateObject(state, {
                isLoading: true
            });
        case actionTypes.FETCH_FLOW_SUCCESS:
            return updateObject(state, {
                isLoading: false,
                blockGroups: action.blockGroups
            });
        case actionTypes.FETCH_FLOW_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error.msg
            });
        default:
            return state
    }
};