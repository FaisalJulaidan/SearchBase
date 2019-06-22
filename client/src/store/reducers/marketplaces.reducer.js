import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {
    marketplacesList: [],
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
        case actionTypes.GET_MARKETPLACES_REQUEST:
            return updateObject(state, {
                isLoadingMarketplaces: true,
            });
        case actionTypes.GET_MARKETPLACES_SUCCESS:
            return updateObject(state, {
                isLoadingMarketplaces: false,
                marketplacesList: action.marketplacesList["crms"],
                companyID: action.marketplacesList["companyID"],
            });
        case actionTypes.GET_MARKETPLACES_FAILURE:
            return updateObject(state, {
                isLoadingMarketplaces: false,
                errorMsg: action.error
            });


        // CONNECT CRM
        case actionTypes.CONNECT_CRM_REQUEST:
            return updateObject(state, {
                isConnecting: true,
            });
        case actionTypes.CONNECT_CRM_SUCCESS:
            tState = {...state};
            tState.marketplacesList.push(action.connectedCRM);
            return updateObject(state, {
                isConnecting: false,
                connectedCRM_ID: action.connectedCRM,
                marketplacesList: tState.marketplacesList
            });
        case actionTypes.CONNECT_CRM_FAILURE:
            return updateObject(state, {
                isConnecting: false,
                errorMsg: action.error
            });

        // TEST CRM
        case actionTypes.TEST_CRM_REQUEST:
            return updateObject(state, {
                isTesting: true,
            });
        case actionTypes.TEST_CRM_SUCCESS:
            return updateObject(state, {
                isTesting: false,
            });
        case actionTypes.TEST_CRM_FAILURE:
            return updateObject(state, {
                isTesting: false,
                errorMsg: action.error
            });

        // DISCONNECT CRM
        case actionTypes.DISCONNECT_CRM_REQUEST:
            return updateObject(state, {
                isDisconnecting: false,
                errorMsg: null,
            });
        case actionTypes.DISCONNECT_CRM_SUCCESS:
            tState = {...state};
            return updateObject(state, {
                isDisconnecting: false,
                connectedCRM_ID: action.connectedCRM_ID,
                marketplacesList: tState.marketplacesList.filter(x => x.ID !== action.connectedCRM_ID)
            });
        case actionTypes.DISCONNECT_CRM_FAILURE:
            return updateObject(state, {
                isDisconnecting: false,
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
