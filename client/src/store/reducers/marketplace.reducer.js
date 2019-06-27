import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {
    connectionStatus: 'NOT_CONNECTED',
    isPinging: false,
    errorMsg: null,
    currentCRM: {},
    isLoadingMarketplaces: false,
    isConnecting: false,
    isTesting: false,
    isDisconnecting: false
};

export const marketplace = (state = initialState, action) => {
    let tState = {};

    switch (action.type) {

        // FETCH MARKETPLACE
        case actionTypes.FETCH_MARKETPLACE_REQUEST:
            return updateObject(state, {});
        case actionTypes.FETCH_MARKETPLACE_SUCCESS:
            return updateObject(state, {});
        case actionTypes.FETCH_MARKETPLACE_FAILURE:
            return updateObject(state, {});

        // PING MARKETPLACE
        case actionTypes.PING_MARKETPLACE_REQUEST:
            return updateObject(state, {
                isPinging: true
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
                isDisconnecting: false,
                errorMsg: null,
            });
        case actionTypes.DISCONNECT_MARKETPLACE_SUCCESS:
            tState = {...state};
            return updateObject(state, {
                isDisconnecting: false,
                connectedCRM_ID: action.connectedCRM_ID,
                marketplacesList: tState.marketplacesList.filter(x => x.ID !== action.connectedCRM_ID)
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
            });
        case actionTypes.CONNECT_MARKETPLACE_SUCCESS:
            tState = {...state};
            tState.marketplacesList.push(action.connectedCRM);
            return updateObject(state, {
                isConnecting: false,
                connectedCRM_ID: action.connectedCRM,
                marketplacesList: tState.marketplacesList
            });
        case actionTypes.CONNECT_MARKETPLACE_FAILURE:
            return updateObject(state, {
                isConnecting: false,
                errorMsg: action.error
            });

        // EXPORT RECRUITER VALUE CRM
        case actionTypes.EXPORT_RECRUITER_VALUE_REPORT_REQUEST:
            return updateObject(state, {
                isLoading: true,
                errorMsg: null,
            });
        case actionTypes.EXPORT_RECRUITER_VALUE_REPORT_SUCCESS:
            tState = {...state};
            return updateObject(state, {
                isLoading: false,
                exportData: action.exportData
            });
        case actionTypes.EXPORT_RECRUITER_VALUE_REPORT_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error
            });

        default:
            return state
    }
};
