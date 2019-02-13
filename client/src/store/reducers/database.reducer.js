import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {isLoading: false, errorMsg: null, databasesList: []};


export const database = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.GET_DATABASES_LIST_REQUEST:
            return updateObject(state, {
                isLoading: true
            });
        case actionTypes.GET_DATABASES_LIST_SUCCESS:
            return updateObject(state, {
                isLoading: false,
                databasesList: action.databasesList
            });
        case actionTypes.GET_DATABASES_LIST_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error.msg
            });

        default:
            return state
    }
};