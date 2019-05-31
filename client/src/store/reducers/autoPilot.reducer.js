import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';
import {deepClone} from "helpers";

const initialState = {autoPilotsList: [], isLoading: false, errorMsg: null};

export const autoPilot = (state = initialState, action) => {
    switch (action.type) {
        // Fetch
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
            const autoPilotsCopy = state.autoPilotsList
                .map(a => a.ID === action.autoPilotID ? {...action.updatedAutoPilot}: a);

            return updateObject(state, {
                successMsg: action.successMsg,
                isLoading: false,
                autoPilotsList: autoPilotsCopy
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
                autoPilotList: autoPilotsList
            });
        case actionTypes.DELETE_AUTOPILOT_FAILURE:
            return updateObject(state, {
                isDeleting: false,
                errorMsg: action.errorMsg
            });
        default:
            return state
    }
};
