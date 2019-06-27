import * as actionTypes from './actionTypes';


const fetchAnalytics = (assistantID, split = "yearly", date) => ({
    type: actionTypes.FETCH_ANALYTICS_REQUEST,
    assistantID
});

const fetchAnalyticsSuccess = (analytics) => ({
    type: actionTypes.FETCH_ANALYTICS_SUCCESS,
    analytics
});

const fetchAnalyticsFailure = (error) => ({
    type: actionTypes.FETCH_ANALYTICS_FAILURE,
    error
});


export const analyticsActions = {
    fetchAnalytics,
    fetchAnalyticsSuccess,
    fetchAnalyticsFailure,
};
