import * as actionTypes from '../actions/actionTypes';
import { updateObject } from '../utility';

const initialState = {
    marketplaceItems: null,

    connectionStatus: 'NOT_CONNECTED',
    activeItem: {},

    isPinging: false,
    isDisconnecting: false,
    isConnecting: false,
    isLoading: false,

    errorMsg: null
};

export const marketplace = (state = initialState, action) => {
    let tState = {};

    switch (action.type) {

        // FETCH MARKETPLACE
        case actionTypes.FETCH_MARKETPLACE_REQUEST:
            return updateObject(state, {});
        case actionTypes.FETCH_MARKETPLACE_SUCCESS:
            return updateObject(state, {
                marketplaceItems: action.marketplaceItems
            });
        case actionTypes.FETCH_MARKETPLACE_FAILURE:
            return updateObject(state, {
                marketplaceItems: null
            });

        case actionTypes.FETCH_MARKETPLACE_ITEM_REQUEST:
            return updateObject(state, { isLoading: true });
        case actionTypes.FETCH_MARKETPLACE_ITEM_SUCCESS:
            return updateObject(state, {
                activeItem: action.activeItem,
                isLoading: false
            });
        case actionTypes.FETCH_MARKETPLACE_ITEM_FAILURE:
            return updateObject(state, {
                marketplaceItems: null,
                isLoading: false
            });

        // Save marketplace
        case actionTypes.SAVE_MARKETPLACE_ITEM_REQUEST:
            return updateObject(state, {
                isLoading: true
            });

        case actionTypes.SAVE_MARKETPLACE_ITEM_SUCCESS:
            return updateObject(state, {
                isLoading: true,
                activeItem: action.activeItem
            });

        case actionTypes.SAVE_MARKETPLACE_ITEM_FAILURE:
            return updateObject(state, {
                isLoading: false
            });
        // PING MARKETPLACE
        case actionTypes.PING_MARKETPLACE_REQUEST:
            return updateObject(state, {
                isPinging: true,
                isDisconnecting: false
            });
        case actionTypes.PING_MARKETPLACE_SUCCESS:
            return updateObject(state, {
                connectionStatus: action.connectionStatus,
                isPinging: false
            });
        case actionTypes.PING_MARKETPLACE_FAILURE:
            return updateObject(state, {
                errorMsg: action.error,
                isPinging: false
            });

        // DISCONNECT MARKETPLACE
        case actionTypes.DISCONNECT_MARKETPLACE_REQUEST:
            return updateObject(state, {
                isDisconnecting: true
            });
        case actionTypes.DISCONNECT_MARKETPLACE_SUCCESS:
            return updateObject(state, {
                connectionStatus: 'NOT_CONNECTED',
                isDisconnecting: false
            });
        case actionTypes.DISCONNECT_MARKETPLACE_FAILURE:
            return updateObject(state, {
                isDisconnecting: false,
                errorMsg: action.error
            });

        // CONNECT MARKETPLACE
        case actionTypes.CONNECT_MARKETPLACE_REQUEST:
            return updateObject(state, {
                isConnecting: true,
                isDisconnecting: false
            });
        case actionTypes.CONNECT_MARKETPLACE_SUCCESS:
            return updateObject(state, {
                connectionStatus: 'CONNECTED',
                isConnecting: false
            });
        case actionTypes.CONNECT_MARKETPLACE_FAILURE:
            return updateObject(state, {
                isConnecting: false,
                errorMsg: action.error
            });

        // EXPORT RECRUITER VALUE CRM
        case actionTypes.EXPORT_RECRUITER_VALUE_REPORT_REQUEST:
            return updateObject(state, {
                errorMsg: null
            });
        case actionTypes.EXPORT_RECRUITER_VALUE_REPORT_SUCCESS:
            tState = { ...state };
            return updateObject(state, {
                exportData: action.exportData
            });
        case actionTypes.EXPORT_RECRUITER_VALUE_REPORT_FAILURE:
            return updateObject(state, {
                errorMsg: action.error
            });

        default:
            return state;
    }
};
