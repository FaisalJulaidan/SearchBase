import * as actionTypes from './actionTypes';


const fetchMarketplace = () => {
    return {
        type: actionTypes.FETCH_MARKETPLACE_REQUEST,
    };
};

const fetchMarketplaceSuccess = () => {
    return {
        type: actionTypes.FETCH_MARKETPLACE_SUCCESS,
    };
};

const fetchMarketplaceFailure = (error) => {
    return {
        type: actionTypes.FETCH_MARKETPLACE_FAILURE,
        error
    };
};

const pingMarketplace = (marketplaceType) => {
    return {
        type: actionTypes.PING_MARKETPLACE_REQUEST,
        marketplaceType
    };
};

const pingMarketplaceSuccess = (connectionStatus) => {
    return {
        type: actionTypes.PING_MARKETPLACE_SUCCESS,
        connectionStatus,
    };
};

const pingMarketplaceFailure = (error) => {
    return {
        type: actionTypes.PING_MARKETPLACE_FAILURE,
        error
    };
};

const connectMarketplace = () => {
    return {
        type: actionTypes.CONNECT_MARKETPLACE_REQUEST,
    };
};

const connectMarketplaceSuccess = (msg) => {
    return {
        type: actionTypes.CONNECT_MARKETPLACE_SUCCESS,
        msg
    };
};

const connectMarketplaceFailure = (error) => {
    return {
        type: actionTypes.CONNECT_MARKETPLACE_FAILURE,
        error
    };
};


const disconnectMarketplace = () => {
    return {
        type: actionTypes.DISCONNECT_MARKETPLACE_REQUEST,
    };
};

const disconnectMarketplaceSuccess = (msg) => {
    return {
        type: actionTypes.DISCONNECT_MARKETPLACE_SUCCESS,
        msg
    };
};

const disconnectMarketplaceFailure = (error) => {
    return {
        type: actionTypes.DISCONNECT_MARKETPLACE_FAILURE,
        error
    };
};


const exportRecruiterValueReport = (connectedCRM_Type) => {
    return {
        type: actionTypes.EXPORT_RECRUITER_VALUE_REPORT_REQUEST,
        connectedCRM_Type
    };
};

const exportRecruiterValueReportSuccess = (exportData) => {
    return {
        type: actionTypes.EXPORT_RECRUITER_VALUE_REPORT_SUCCESS,
        exportData
    };
};

const exportRecruiterValueReportFailure = (error) => {
    return {
        type: actionTypes.EXPORT_RECRUITER_VALUE_REPORT_FAILURE,
        error
    };
};


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
