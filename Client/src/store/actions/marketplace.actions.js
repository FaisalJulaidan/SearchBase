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

const fetchMarketplaceItem = (marketplaceType) => ({
    type: actionTypes.FETCH_MARKETPLACE_ITEM_REQUEST,
    marketplaceType
})

const fetchMarketplaceItemSuccess = (activeItem) => ({
    type: actionTypes.FETCH_MARKETPLACE_ITEM_SUCCESS,
    activeItem
})

const fetchMarketplaceItemFailure = () => ({
    type: actionTypes.FETCH_MARKETPLACE_ITEM_FAILURE
})

const saveMarketplaceItem = (marketplaceType, CRMAutoPilotID) => ({
    type: actionTypes.SAVE_MARKETPLACE_ITEM_REQUEST,
    marketplaceType,
    CRMAutoPilotID
})

const saveMarketplaceItemSuccess = (activeItem) => ({
    type: actionTypes.SAVE_MARKETPLACE_ITEM_SUCCESS,
    activeItem
})

const saveMarketplaceItemFailure = () => ({
    type: actionTypes.SAVE_MARKETPLACE_ITEM_FAILURE
})


const pingMarketplace = (marketplaceType) => ({
    type: actionTypes.PING_MARKETPLACE_REQUEST,
    meta: {thunk: true},
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

    fetchMarketplaceItem,
    fetchMarketplaceItemSuccess,
    fetchMarketplaceItemFailure,

    saveMarketplaceItem,
    saveMarketplaceItemFailure,
    saveMarketplaceItemSuccess,

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
