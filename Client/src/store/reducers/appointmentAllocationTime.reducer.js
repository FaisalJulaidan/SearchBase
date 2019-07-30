import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {allocationTimes: [], isLoading: true, errorMsg: null};

export const appointmentAllocationTime = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.FETCH_AAT_REQUEST:
            return updateObject(state, {
                allocationTimes: [],
                isLoading: true,
            });
        case actionTypes.FETCH_AAT_SUCCESS:
            return updateObject(state, {
                allocationTimes: action.allocationTimes,
                isLoading: false
            });
        case actionTypes.FETCH_AAT_FAILURE:
            return updateObject(state, {
                allocationTimes: [],
                isLoading: false,
                errorMsg: action.error
            });

        default:
            return state
    }
};
