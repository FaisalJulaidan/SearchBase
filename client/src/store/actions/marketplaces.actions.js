import * as actionTypes from './actionTypes';

const getConnectedCRMs = () => {
    return {
        type: actionTypes.GET_MARKETPLACES_REQUEST,
    };
};

const getConnectedCRMsSuccess = (marketplacesList, companyID, msg) => {
    return {
        type: actionTypes.GET_MARKETPLACES_SUCCESS,
        marketplacesList,
        companyID,
        msg
    };
};

const getConnectedCRMsFailure = (error) => {
    return {
        type: actionTypes.GET_MARKETPLACES_FAILURE,
        error
    };
};

const connectMarketplace = (connectedCRM) => {
    return {
        type: actionTypes.CONNECT_MARKETPLACE_REQUEST,
        connectedCRM
    };
};

const connectMarketplaceSuccess = (connectedCRM, msg) => {
    return {
        type: actionTypes.CONNECT_MARKETPLACE_SUCCESS,
        connectedCRM,
        msg
    };
};

const connectMarketplaceFailure = (error) => {
    return {
        type: actionTypes.CONNECT_MARKETPLACE_FAILURE,
        error
    };
};

const testMarketplace = (testedCRM) => {
    return {
        type: actionTypes.TEST_MARKETPLACE_REQUEST,
        testedCRM
    };
};

const testMarketplaceSuccess = () => {
    return {
        type: actionTypes.TEST_MARKETPLACE_SUCCESS,
    };
};

const testMarketplaceFailure = (error) => {
    return {
        type: actionTypes.TEST_MARKETPLACE_FAILURE,
        error
    };
};

const disconnectMarketplace = (disconnectedCRMID) => {
    return {
        type: actionTypes.DISCONNECT_MARKETPLACE_REQUEST,
        disconnectedCRMID
    };
};

const disconnectMarketplaceSuccess = (connectedCRM_ID, msg) => {
    return {
        type: actionTypes.DISCONNECT_MARKETPLACE_SUCCESS,
        connectedCRM_ID,
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


export const marketplacesActions = {
    getConnectedCRMs,
    getConnectedCRMsSuccess,
    getConnectedCRMsFailure,

    connectMarketplace,
    connectMarketplaceSuccess,
    connectMarketplaceFailure,

    testMarketplace,
    testMarketplaceSuccess,
    testMarketplaceFailure,

    disconnectMarketplace,
    disconnectMarketplaceSuccess,
    disconnectMarketplaceFailure,

    exportRecruiterValueReport,
    exportRecruiterValueReportSuccess,
    exportRecruiterValueReportFailure

};
