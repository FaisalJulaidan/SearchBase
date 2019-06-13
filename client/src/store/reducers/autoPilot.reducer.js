import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';
import {deepClone} from "helpers";

const initialState = {autoPilotsList: [], autoPilot: null, isLoading: false, errorMsg: null};

export const autoPilot = (state = initialState, action) => {
    switch (action.type) {
        // Fetch All
        case actionTypes.FETCH_AUTOPILOTS_REQUEST:
            return updateObject(state, {
                autoPilotsList: [],
                errorMsg: null,
                isLoading: true,
            });
        case actionTypes.FETCH_AUTOPILOTS_SUCCESS:
            return updateObject(state, {
                autoPilotsList: action.autoPilotsList,
                isLoading: false
            });
        case actionTypes.FETCH_AUTOPILOTS_FAILURE:
            return updateObject(state, {
                autoPilotsList: [],
                isLoading: false,
                errorMsg: action.errorMsg
            });


        // Fetch
        case actionTypes.FETCH_AUTOPILOT_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isLoading: true,
            });
        case actionTypes.FETCH_AUTOPILOT_SUCCESS:
            return updateObject(state, {
                autoPilot: action.autoPilot,
                isLoading: false
            });
        case actionTypes.FETCH_AUTOPILOT_FAILURE:
            return updateObject(state, {
                autoPilot: null,
                isLoading: false,
                errorMsg: action.errorMsg
            });


        // Add
        case actionTypes.ADD_AUTOPILOT_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isAdding: true
            });
        case actionTypes.ADD_AUTOPILOT_SUCCESS:

            return updateObject(state, {
                successMsg: action.successMsg,
                isAdding: false,
                autoPilotsList: state.autoPilotsList.concat(action.newAutoPilot)
            });
        case actionTypes.ADD_AUTOPILOT_FAILURE:
            return updateObject(state, {
                isAdding: false,
                errorMsg: action.errorMsg
            });

        // Update
        case actionTypes.UPDATE_AUTOPILOT_REQUEST:
            return updateObject(state, {
                successMsg: null,
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.UPDATE_AUTOPILOT_SUCCESS:
            return updateObject(state, {
                successMsg: action.successMsg,
                isLoading: false,
                autoPilot: action.updatedAutoPilot
            });
        case actionTypes.UPDATE_AUTOPILOT_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.errorMsg
            });

        // Delete
        case actionTypes.DELETE_AUTOPILOT_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isDeleting: true
            });

        case actionTypes.DELETE_AUTOPILOT_SUCCESS:
            let autoPilotsList = [...state.autoPilotsList].filter(autoPilot => autoPilot.ID !== action.autoPilotID);
            return updateObject(state, {
                successMsg: action.successMsg,
                isDeleting: false,
                autoPilotList: autoPilotsList,
                autoPilot: null
            });

        case actionTypes.DELETE_AUTOPILOT_FAILURE:
            return updateObject(state, {
                isDeleting: false,
                errorMsg: action.errorMsg
            });

        // Update Status
        case actionTypes.UPDATE_AUTOPILOT_STATUS_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isStatusChanging: true
            });

        case actionTypes.UPDATE_AUTOPILOT_STATUS_SUCCESS:
            return updateObject(state, {
                successMsg: action.successMsg,
                isStatusChanging: false,
                autoPilot: {...state.autoPilot, Active: action.status}
            });

        case actionTypes.UPDATE_AUTOPILOT_STATUS_FAILURE:
            return updateObject(state, {
                isStatusChanging: false,
                errorMsg: action.error
            });

        default:
            return state
    }
};
