import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {CRMsList: [], errorMsg: null};

export const crmlist = (state = initialState, action) => {
    state = initialState;
    switch (action.type) {
        case actionTypes.GET_CONNECTED_CRMS_REQUEST:
            return updateObject(state, {
                errorMsg: null,
            });
        case actionTypes.GET_CONNECTED_CRMS_SUCCESS:
            return updateObject(state, {
                CRMsList: action.CRMsList,
            });
        case actionTypes.GET_CONNECTED_CRMS_FAILURE:
            return updateObject(state, {
                errorMsg: action.error
            });
        default:
            return state
    }
};
