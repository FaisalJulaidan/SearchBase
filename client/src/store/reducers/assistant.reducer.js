import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';
import {deepClone} from "helpers";

const initialState = {assistantList: [], assistant: null, isLoading: false, errorMsg: null, isUpdatingFlow: false};


export const assistant = (state = initialState, action) => {


    switch (action.type) {
        // Fetch All
        case actionTypes.FETCH_ASSISTANTS_REQUEST:
            return updateObject(state, {
                assistantList: [],
                assistant: null,
                errorMsg: null,
                isLoading: true,
            });
        case actionTypes.FETCH_ASSISTANTS_SUCCESS:
            return updateObject(state, {
                assistantList: action.assistantList,
                isLoading: false
            });
        case actionTypes.FETCH_ASSISTANTS_FAILURE:
            return updateObject(state, {
                assistantList: [],
                isLoading: false,
                errorMsg: action.error
            });

        // Fetch One with more details
        case actionTypes.FETCH_ASSISTANT_REQUEST:
            return updateObject(state, {
                assistant: null,
                errorMsg: null,
                isLoading: true,
            });
        case actionTypes.FETCH_ASSISTANT_SUCCESS:
            return updateObject(state, {
                assistant: action.assistant,
                isLoading: false
            });
        case actionTypes.FETCH_ASSISTANT_FAILURE:
            return updateObject(state, {
                assistant: null,
                isLoading: false,
                errorMsg: action.error
            });


        // Add
        case actionTypes.ADD_ASSISTANT_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isAdding: true
            });
        case actionTypes.ADD_ASSISTANT_SUCCESS:

            return updateObject(state, {
                successMsg: action.successMsg,
                isAdding: false,
                assistantList: state.assistantList.concat(action.newAssistant)
            });
        case actionTypes.ADD_ASSISTANT_FAILURE:
            return updateObject(state, {
                isAdding: false,
                errorMsg: action.error
            });


        // Simple Update
        case actionTypes.UPDATE_ASSISTANT_REQUEST:

            return updateObject(state, {
                successMsg: null,
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.UPDATE_ASSISTANT_SUCCESS:
            return updateObject(state, {
                successMsg: action.successMsg,
                isLoading: false,
                assistantList: state.assistantList
                    .map(a => a.ID === action.assistantID ? {...action.updatedAssistant}: a)
            });
        case actionTypes.UPDATE_ASSISTANT_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error
            });


        // Update
        case actionTypes.UPDATE_ASSISTANT_CONFIGS_REQUEST:

            return updateObject(state, {
                successMsg: null,
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.UPDATE_ASSISTANT_CONFIGS_SUCCESS:
            return updateObject(state, {
                successMsg: action.successMsg,
                isLoading: false,
                assistant: action.updatedAssistant
            });
        case actionTypes.UPDATE_ASSISTANT_CONFIGS_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error
            });


        // Delete
        case actionTypes.DELETE_ASSISTANT_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isDeleting: true
            });
        case actionTypes.DELETE_ASSISTANT_SUCCESS:
            return updateObject(state, {
                successMsg: action.successMsg,
                isDeleting: false,
                assistantList: [...state.assistantList].filter(assistant => assistant.ID !== action.assistantID)
            });
        case actionTypes.DELETE_ASSISTANT_FAILURE:
            return updateObject(state, {
                isDeleting: false,
                errorMsg: action.error
            });

        // Change Status (On, Off)
        case actionTypes.CHANGE_ASSISTANT_STATUS_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isStatusChanging: true
            });
        case actionTypes.CHANGE_ASSISTANT_STATUS_SUCCESS:
            return updateObject(state, {
                successMsg: action.successMsg,
                isStatusChanging: false,
                assistant: {...state.assistant, Active: action.status}
            });
        case actionTypes.CHANGE_ASSISTANT_STATUS_FAILURE:
            return updateObject(state, {
                isStatusChanging: false,
                errorMsg: action.error
            });

         // Update Flow (Script)
        case actionTypes.UPDATE_FLOW_REQUEST:
            return updateObject(state, {
                isUpdatingFlow: true,
                updateFlowSuccessMsg: null,
                updateFlowErrorMsg: null,
            });
        case actionTypes.UPDATE_FLOW_SUCCESS:

            let newAssistantList = deepClone(state.assistantList);
            newAssistantList =  newAssistantList.filter(assistant => assistant.id !== action.assistant.id);
            newAssistantList.push(action.assistant);

            return updateObject(state, {
                isUpdatingFlow: false,
                updateFlowSuccessMsg: action.msg,
                assistantList: newAssistantList
            });
        case actionTypes.UPDATE_FLOW_FAILURE:
            return updateObject(state, {
                isUpdatingFlow: false,
                updateFlowErrorMsg: action.error
            });

        // CRM Connection
        // Connect
        case actionTypes.CONNECT_ASSISTANT_TO_CRM_REQUEST:
            return updateObject(state, {
                errorMsg: null,
            });
        case actionTypes.CONNECT_ASSISTANT_TO_CRM_SUCCESS:
            return updateObject(state, {
                assistant: {...state.assistant, CRMID: action.CRMID}
            });
        case actionTypes.CONNECT_ASSISTANT_TO_CRM_FAILURE:
            return updateObject(state, {
                errorMsg: action.error
            });

        // Disconnect
        case actionTypes.DISCONNECT_ASSISTANT_FROM_CRM_REQUEST:
            return updateObject(state, {
                errorMsg: null,
            });
        case actionTypes.DISCONNECT_ASSISTANT_FROM_CRM_SUCCESS:
            return updateObject(state, {
                assistant: {...state.assistant, CRMID: null}
            });

        case actionTypes.DISCONNECT_ASSISTANT_FROM_CRM_FAILURE:
            return updateObject(state, {
                errorMsg: action.error
            });


        // Calendar Connection
        // Connect
        case actionTypes.CONNECT_ASSISTANT_TO_CALENDAR_REQUEST:
            return updateObject(state, {
                errorMsg: null,
            });
        case actionTypes.CONNECT_ASSISTANT_TO_CALENDAR_SUCCESS:
            return updateObject(state, {
                assistant: {...state.assistant, CalendarID: action.calendarID}
            });
        case actionTypes.CONNECT_ASSISTANT_TO_CALENDAR_FAILURE:
            return updateObject(state, {
                errorMsg: action.error
            });

        // Disconnect
        case actionTypes.DISCONNECT_ASSISTANT_FROM_CALENDAR_REQUEST:
            return updateObject(state, {
                errorMsg: null,
            });
        case actionTypes.DISCONNECT_ASSISTANT_FROM_CALENDAR_SUCCESS:
            return updateObject(state, {
                assistant: {...state.assistant, CalendarID: null}
            });

        case actionTypes.DISCONNECT_ASSISTANT_FROM_CALENDAR_FAILURE:
            return updateObject(state, {
                errorMsg: action.error
            });



        // AutoPilot Connection
        // Connect
        case actionTypes.CONNECT_ASSISTANT_TO_AUTO_PILOT_REQUEST:
            return updateObject(state, {
                errorMsg: null,
            });
        case actionTypes.CONNECT_ASSISTANT_TO_AUTO_PILOT_SUCCESS:
            return updateObject(state, {
                assistant: {...state.assistant, AutoPilotID: action.autoPilotID}
            });
        case actionTypes.CONNECT_ASSISTANT_TO_AUTO_PILOT_FAILURE:
            return updateObject(state, {
                errorMsg: action.error,
            });

        // Disconnect
        case actionTypes.DISCONNECT_ASSISTANT_FROM_AUTO_PILOT_REQUEST:
            return updateObject(state, {
                errorMsg: null,
            });
        case actionTypes.DISCONNECT_ASSISTANT_FROM_AUTO_PILOT_SUCCESS:
            return updateObject(state, {
                assistant: {...state.assistant, AutoPilotID: null}
            });
        case actionTypes.DISCONNECT_ASSISTANT_FROM_AUTO_PILOT_FAILURE:
            return updateObject(state, {
                errorMsg: action.error
            });

        default:
            return state
    }
};
