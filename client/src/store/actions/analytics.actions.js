import * as actionTypes from './actionTypes';


const fetchAnalytics = () => {
    return {
        type: actionTypes.FETCH_ANALYTICS_REQUEST
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


export const assistantActions = {
    fetchAnalytics,
    fetchAnalyticsSuccess,
    fetchAnalyticsFailure,


};