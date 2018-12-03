import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {assistantList: []};

export const assistant = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.FETCH_ASSISTANTS_SUCCESS:
            return updateObject(state, {assistantList: action.assistantList});
        case actionTypes.FETCH_ASSISTANTS_FAILURE:
            return updateObject(state, {assistantList: []});
        default:
            return state
    }
};