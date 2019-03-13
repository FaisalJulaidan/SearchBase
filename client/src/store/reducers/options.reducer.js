import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState ={options: null, isLoading: false, errorMsg: null};

export const options = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.FETCH_OPTIONS_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isLoading: true,
            });
        case actionTypes.FETCH_OPTIONS_SUCCESS:
            return updateObject(state, {
                isLoading: false,
                options: action.options
            });
        case actionTypes.FETCH_OPTIONS_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error
            });
        default:
            return state
    }
};