import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';
import {deepClone} from "helpers";

const initialState = {assistantList: [], assistant: null, isLoading: false, errorMsg: null, isUpdatingFlow: false};


export const assistant = (state = initialState, action) => {

    let assistantsCopy;
    let index;

    switch (action.type) {
        // Fetch
        case actionTypes.FETCH_ASSISTANTS_REQUEST:
            return updateObject(state, {
                assistantList: [],
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



        // Update
        case actionTypes.UPDATE_ASSISTANT_REQUEST:

            return updateObject(state, {
                successMsg: null,
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.UPDATE_ASSISTANT_SUCCESS:
            assistantsCopy = state.assistantList
                .map(a => a.ID === action.assistantID ? {...action.updatedAssistant}: a);

            return updateObject(state, {
                successMsg: action.successMsg,
                isLoading: false,
                assistantList: assistantsCopy
            });
        case actionTypes.UPDATE_ASSISTANT_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error
            });

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

            let assistantList = [...state.assistantList].filter(assistant => assistant.ID !== action.assistantID);
            return updateObject(state, {
                successMsg: action.successMsg,
                isDeleting: false,
                assistantList
            });
        case actionTypes.DELETE_ASSISTANT_FAILURE:
            return updateObject(state, {
                isDeleting: false,
                errorMsg: action.error
            });


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


        case actionTypes.SELECT_ASSISTANT_CRM_REQUEST:
            return updateObject(state, {
                errorMsg: null,
            });
        case actionTypes.SELECT_ASSISTANT_CRM_SUCCESS:
            return updateObject(state, {});
        case actionTypes.SELECT_ASSISTANT_CRM_FAILURE:
            return updateObject(state, {
                errorMsg: action.error
            });

        case actionTypes.RESET_ASSISTANT_CRM_REQUEST:
            return updateObject(state, {
                errorMsg: null,
            });
        case actionTypes.RESET_ASSISTANT_CRM_SUCCESS:
            return updateObject(state, {});
        case actionTypes.RESET_ASSISTANT_CRM_FAILURE:
            return updateObject(state, {
                errorMsg: action.error
            });

        case actionTypes.SELECT_AUTO_PILOT_REQUEST:
            return updateObject(state, {
                errorMsg: null,
            });
        case actionTypes.SELECT_AUTO_PILOT_SUCCESS:

            assistantsCopy = deepClone(state.assistantList);
            index = assistantsCopy.findIndex(x => x.ID === action.assistantID);
            assistantsCopy[index].AutoPilotID = action.autoPilotID;

            return updateObject(state, {
                assistantList: assistantsCopy
            });
        case actionTypes.SELECT_AUTO_PILOT_FAILURE:
            return updateObject(state, {
                errorMsg: action.error,
            });


        case actionTypes.DISCONNECT_AUTO_PILOT_REQUEST:
            return updateObject(state, {
                errorMsg: null,
            });
        case actionTypes.DISCONNECT_AUTO_PILOT_SUCCESS:

            assistantsCopy = deepClone(state.assistantList);
            index = assistantsCopy.findIndex(x => x.ID === action.assistantID);
            assistantsCopy[index].AutoPilotID = null;

            return updateObject(state, {
                assistantList: assistantsCopy
            });
        case actionTypes.DISCONNECT_AUTO_PILOT_FAILURE:
            return updateObject(state, {
                errorMsg: action.error
            });



        default:
            return state
    }
};
