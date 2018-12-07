import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {isLoading: false, errorMsg: null};

export const settings = (state = initialState, action) => {
    console.log(action)
    switch (action.type) {
        case actionTypes.UPDATE_ASSISTANT_SETTINGS_REQUEST:
            return updateObject(state, {
                successMsg: null,
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.UPDATE_ASSISTANT_SETTINGS_SUCCESS:
            return updateObject(state, {
                successMsg: action.successMsg,
                isLoading: false
            });
        case actionTypes.UPDATE_ASSISTANT_SETTINGS_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error.msg
            });
        default:
            return state
    }
};