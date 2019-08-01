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
                newSettings: action.newSettings
            });
        case actionTypes.SAVE_AAT_SUCCESS:
            return updateObject(state, {
                isLoading: false,
                aat: null
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
        case actionTypes.DELETE_AAT_REQUEST:
            return updateObject(state, {
                isLoading: true
            });
        case actionTypes.DELETE_AAT_SUCCESS:
            console.log(action)
            return updateObject(state, {
                isLoading: false,
                allocationTimes: state.allocationTimes.filter(aat => aat.ID !== parseInt(action.id))
            });
        case actionTypes.DELETE_AAT_FAILURE:
            return updateObject(state, {
                errorMsg: action.error
            });
        default:
            return state
    }
};
