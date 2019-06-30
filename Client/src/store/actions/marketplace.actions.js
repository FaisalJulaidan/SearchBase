import * as actionTypes from './actionTypes';


const fetchMarketplace = () => ({
    type: actionTypes.FETCH_MARKETPLACE_REQUEST,
});

const fetchMarketplaceSuccess = (marketplaceItems) => ({
    type: actionTypes.FETCH_MARKETPLACE_SUCCESS,
    marketplaceItems
});

const fetchMarketplaceFailure = (error) => ({
    type: actionTypes.FETCH_MARKETPLACE_FAILURE,
    error
});

const pingMarketplace = (marketplaceType) => ({
    type: actionTypes.PING_MARKETPLACE_REQUEST,
    marketplaceType
});

const pingMarketplaceSuccess = (connectionStatus) => ({
    type: actionTypes.PING_MARKETPLACE_SUCCESS,
    connectionStatus,
});

const pingMarketplaceFailure = (error) => ({
    type: actionTypes.PING_MARKETPLACE_FAILURE,
    error
});

const connectMarketplace = (marketplaceType, auth) => ({
    type: actionTypes.CONNECT_MARKETPLACE_REQUEST,
    marketplaceType,
    auth
});

const connectMarketplaceSuccess = () => ({
    type: actionTypes.CONNECT_MARKETPLACE_SUCCESS,
});

const connectMarketplaceFailure = (error) => ({
    type: actionTypes.CONNECT_MARKETPLACE_FAILURE,
    error
});


const disconnectMarketplace = (marketplaceType) => ({
    type: actionTypes.DISCONNECT_MARKETPLACE_REQUEST,
    marketplaceType
});

const disconnectMarketplaceSuccess = (msg) => ({
    type: actionTypes.DISCONNECT_MARKETPLACE_SUCCESS,
    msg
});

const disconnectMarketplaceFailure = (error) => ({
    type: actionTypes.DISCONNECT_MARKETPLACE_FAILURE,
    error
});


const exportRecruiterValueReport = (connectedCRM_Type) => ({
    type: actionTypes.EXPORT_RECRUITER_VALUE_REPORT_REQUEST,
    connectedCRM_Type
});

const exportRecruiterValueReportSuccess = (exportData) => ({
    type: actionTypes.EXPORT_RECRUITER_VALUE_REPORT_SUCCESS,
    exportData
});

const exportRecruiterValueReportFailure = (error) => ({
    type: actionTypes.EXPORT_RECRUITER_VALUE_REPORT_FAILURE,
    error
});


export const marketplaceActions = {
    fetchMarketplace,
    fetchMarketplaceSuccess,
    fetchMarketplaceFailure,

    pingMarketplace,
    pingMarketplaceSuccess,
    pingMarketplaceFailure,

    connectMarketplace,
    connectMarketplaceSuccess,
    connectMarketplaceFailure,

    disconnectMarketplace,
    disconnectMarketplaceSuccess,
    disconnectMarketplaceFailure,

    exportRecruiterValueReport,
    exportRecruiterValueReportSuccess,
    exportRecruiterValueReportFailure
};