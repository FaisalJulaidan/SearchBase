import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {CRMsList: [], errorMsg: null, currentCRM: {}};

export const crm = (state = initialState, action) => {
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


        // CONNECT CRM
        case actionTypes.CONNECT_CRM_REQUEST:
            return updateObject(state, {
                errorMsg: null,
            });
        case actionTypes.CONNECT_CRM_SUCCESS:
            return updateObject(state, {
                connectedCRM_ID: action.connectedCRM_ID
            });
        case actionTypes.CONNECT_CRM_FAILURE:
            return updateObject(state, {
                errorMsg: action.error
            });

        // TEST CRM
        case actionTypes.TEST_CRM_REQUEST:
            return updateObject(state, {
                errorMsg: null,
            });
        case actionTypes.TEST_CRM_SUCCESS:
            return updateObject(state, {});
        case actionTypes.TEST_CRM_FAILURE:
            return updateObject(state, {
                errorMsg: action.error
            });

        case actionTypes.DISCONNECT_CRM_REQUEST:
            return updateObject(state, {
                errorMsg: null,
            });
        case actionTypes.DISCONNECT_CRM_SUCCESS:
            return updateObject(state, {
                connectedCRM_ID: action.connectedCRM_ID
            });
        case actionTypes.DISCONNECT_CRM_FAILURE:
            return updateObject(state, {
                errorMsg: action.error
            });

        default:
            return state
    }
};