import * as actionTypes from './actionTypes';


const fetchAnalytics = (assistantID, split="yearly") => {
    return {
        type: actionTypes.FETCH_ANALYTICS_REQUEST,
        assistantID,
        split
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