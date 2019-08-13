import * as actionTypes from "./actionTypes";
const fetchDevRequest = () => {
    return {
        type: actionTypes.FETCH_DEV_REQUEST,
    };
};

const fetchDevSuccess = (webhooks) => {
    return {
        type: actionTypes.FETCH_DEV_SUCCESS,
        webhooks
    };
};

const fetchDevFailure = (error) => {
    return {
        type: actionTypes.FETCH_DEV_FAILURE,
        error
    };
};

const createWebhookRequest = (ID, settings) => {
    return {
        type: actionTypes.CREATE_WEBHOOK_REQUEST,
        ID,
        settings
    };
};

const createWebhookSuccess = (webhook) => {
    return {
        type: actionTypes.CREATE_WEBHOOK_SUCCESS,
        webhook
    };
}

const createWebhookFailure = (error) => {
    return {
        type: actionTypes.CREATE_WEBHOOK_FAILURE,
        error
    };
}

const saveWebhookRequest = (ID, newSettings) => {
    return {
        type: actionTypes.SAVE_WEBHOOK_REQUEST,
        ID,
        newSettings
    };
};

const saveWebhookSuccess = () => {
    return {
        type: actionTypes.SAVE_WEBHOOK_SUCCESS,
    };
}

const saveWebhookFailure = (error) => {
    return {
        type: actionTypes.SAVE_WEBHOOK_FAILURE,
        error
    };
}

export const developmentActions = {
    fetchDevRequest,
    fetchDevSuccess,
    fetchDevFailure,

    createWebhookRequest,
    createWebhookSuccess,
    createWebhookFailure,

    saveWebhookRequest,
    saveWebhookSuccess,
    saveWebhookFailure,
};
