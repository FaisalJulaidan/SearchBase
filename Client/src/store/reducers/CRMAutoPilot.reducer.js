import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {CRMAutoPilotsList: [], CRMAutoPilot: null, isLoading: false, errorMsg: null};

export const CRMAutoPilot = (state = initialState, action) => {

    switch (action.type) {
        // Fetch All
        case actionTypes.FETCH_CRM_AUTOPILOTS_REQUEST:
            return updateObject(state, {
                CRMAutoPilotsList: [],
                errorMsg: null,
                isLoading: true,
            });
        case actionTypes.FETCH_CRM_AUTOPILOTS_SUCCESS:
            return updateObject(state, {
                CRMAutoPilotsList: action.CRMAutoPilotsList,
                isLoading: false
            });
        case actionTypes.FETCH_CRM_AUTOPILOTS_FAILURE:
            return updateObject(state, {
                CRMAutoPilotsList: [],
                isLoading: false,
                errorMsg: action.errorMsg
            });


        // Fetch
        case actionTypes.FETCH_CRM_AUTOPILOT_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isLoading: true,
            });
        case actionTypes.FETCH_CRM_AUTOPILOT_SUCCESS:
            return updateObject(state, {
                CRMAutoPilot: action.CRMAutoPilot,
                isLoading: false
            });
        case actionTypes.FETCH_CRM_AUTOPILOT_FAILURE:
            return updateObject(state, {
                CRMAutoPilot: null,
                isLoading: false,
                errorMsg: action.errorMsg
            });


        // Add
        case actionTypes.ADD_CRM_AUTOPILOT_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isAdding: true
            });
        case actionTypes.ADD_CRM_AUTOPILOT_SUCCESS:

            return updateObject(state, {
                successMsg: action.successMsg,
                isAdding: false,
                CRMAutoPilotsList: state.CRMAutoPilotsList.concat(action.newCRMAutoPilot)
            });
        case actionTypes.ADD_CRM_AUTOPILOT_FAILURE:
            return updateObject(state, {
                isAdding: false,
                errorMsg: action.errorMsg
            });

        // Update
        case actionTypes.UPDATE_CRM_AUTOPILOT_REQUEST:
            return updateObject(state, {
                successMsg: null,
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.UPDATE_CRM_AUTOPILOT_SUCCESS:
            return updateObject(state, {
                successMsg: action.successMsg,
                isLoading: false,
                CRMAutoPilotsList: state.CRMAutoPilotsList
                    .map(a => a.ID === action.CRMAutoPilotID ? {...action.updatedCRMAutoPilot}: a)
            });
        case actionTypes.UPDATE_CRM_AUTOPILOT_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.errorMsg
            });

        // Update Extended Configs
        case actionTypes.UPDATE_CRM_AUTOPILOT_CONFIGS_REQUEST:
            return updateObject(state, {
                successMsg: null,
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.UPDATE_CRM_AUTOPILOT_CONFIGS_SUCCESS:
            return updateObject(state, {
                successMsg: action.successMsg,
                isLoading: false,
                CRMAutoPilot: action.CRMUpdatedAutoPilot
            });
        case actionTypes.UPDATE_CRM_AUTOPILOT_CONFIGS_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.errorMsg
            });


        // Delete
        case actionTypes.DELETE_CRM_AUTOPILOT_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isDeleting: true
            });

        case actionTypes.DELETE_CRM_AUTOPILOT_SUCCESS:
            return updateObject(state, {
                successMsg: action.successMsg,
                isDeleting: false,
                CRMAutoPilotsList: [...state.CRMAutoPilotsList].filter(autoPilot => autoPilot.ID !== action.CRMAutoPilotID),
                CRMAutoPilot: null
            });

        case actionTypes.DELETE_CRM_AUTOPILOT_FAILURE:
            return updateObject(state, {
                isDeleting: false,
                errorMsg: action.errorMsg
            });

        // Update Status
        case actionTypes.UPDATE_CRM_AUTOPILOT_STATUS_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isStatusChanging: true
            });

        case actionTypes.UPDATE_CRM_AUTOPILOT_STATUS_SUCCESS:
            return updateObject(state, {
                successMsg: action.successMsg,
                isStatusChanging: false,
                CRMAutoPilot: {...state.CRMAutoPilot, Active: action.status}
            });

        case actionTypes.UPDATE_CRM_AUTOPILOT_STATUS_FAILURE:
            return updateObject(state, {
                isStatusChanging: false,
                errorMsg: action.error
            });

        default:
            return state
    }
};
