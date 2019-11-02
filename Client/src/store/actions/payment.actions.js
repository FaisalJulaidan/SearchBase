import * as actionTypes from './actionTypes';


const generateCheckoutSession = (companyID, plan) => ({
    type: actionTypes.GENERATE_CHECKOUT_SESSION_REQUEST,
    companyID,
    plan
});

const generateCheckoutSessionSuccess = (sessionID) => ({
    type: actionTypes.GENERATE_CHECKOUT_SESSION_SUCCESS,
    sessionID
});

const generateCheckoutSessionFailure = (error) => ({
    type: actionTypes.GENERATE_CHECKOUT_SESSION_FAILURE,
    error
});


export const paymentActions = {
    generateCheckoutSession,
    generateCheckoutSessionSuccess,
    generateCheckoutSessionFailure,
};
