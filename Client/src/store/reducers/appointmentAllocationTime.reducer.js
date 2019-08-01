import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {allocationTimes: [], isLoading: true, errorMsg: null};

export const appointmentAllocationTime = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.FETCH_AAT_REQUEST:
            return updateObject(state, {
                allocationTimes: [],
                aat: null,
                isLoading: true,
            });
        case actionTypes.FETCH_AAT_SUCCESS:
            console.log(action)
            return updateObject(state, {
                allocationTimes: action.allocationTimes,
                aat: action.aat,
                isLoading: false
            });
        case actionTypes.FETCH_AAT_FAILURE:
            return updateObject(state, {
                allocationTimes: [],
                isLoading: false,
                errorMsg: action.error
            });
        case actionTypes.SAVE_AAT_REQUEST:
            return updateObject(state, {
                isLoading: true,
                newSettings: action.newSetttings
            });
        case actionTypes.SAVE_AAT_SUCCESS:
            return updateObject(state, {
                isLoading: false
            });
        case actionTypes.SAVE_AAT_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error
            });
        case actionTypes.CREATE_AAT_REQUEST:
            return updateObject(state, {
                isLoading: true,
            });
        case actionTypes.CREATE_AAT_SUCCESS:
            return updateObject(state, {
                isLoading: false,
                allocationTimes: state.allocationTimes.concat([action.aat]),
                aat: action.aat
            });
        case actionTypes.CREATE_AAT_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error
            });
        case actionTypes.SWITCH_ACTIVE_AAT:
            console.log(action)
            return updateObject(state, {
                aat: state.allocationTimes.find(aat => aat.ID == action.id)
            });
        default:
            return state
    }
};
