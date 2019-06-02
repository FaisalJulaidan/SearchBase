import * as actionTypes from './actionTypes';


const fetchAnalytics = (assistantID) => {
    return {
        type: actionTypes.FETCH_ANALYTICS_REQUEST,
        assistantID
    };
};

const fetchAnalyticsSuccess = (analytics) => {
    return {
        type: actionTypes.FETCH_ANALYTICS_SUCCESS,
        analytics
    };
};

const fetchAnalyticsFailure = (error) => {
    return {
        type: actionTypes.FETCH_ANALYTICS_FAILURE,
        error
    };
};


export const analyticsActions = {
    fetchAnalytics,
    fetchAnalyticsSuccess,
    fetchAnalyticsFailure,
};