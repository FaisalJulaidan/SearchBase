import * as actionTypes from "./actionTypes";
const fetchDevRequest = () => {
    return {
        type: actionTypes.FETCH_DEV_REQUEST,
    };
};

const fetchDevSuccess = (webhooks, availableWebhooks) => {
    return {
        type: actionTypes.FETCH_DEV_SUCCESS,
        webhooks,
        availableWebhooks
    };
};

const fetchDevFailure = (error) => {
    return {
        type: actionTypes.FETCH_DEV_FAILURE,
        error
    };
};

const createWebhookRequest = (settings) => {
    return {
        type: actionTypes.CREATE_WEBHOOK_REQUEST,
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

const saveWebhookSuccess = (ID) => {
    return {
        type: actionTypes.SAVE_WEBHOOK_SUCCESS,
        ID,
    };
}

const saveWebhookFailure = (error, ID) => {
    return {
        type: actionTypes.SAVE_WEBHOOK_FAILURE,
        error,
        ID
    };
}

const deleteWebhookRequest = (ID) => {
    return {
        type: actionTypes.DELETE_WEBHOOK_REQUEST,
        ID,
    };
}

const deleteWebhookSuccess = (ID) => {
    return {
        type: actionTypes.DELETE_WEBHOOK_SUCCESS,
        ID,
    };
}


const deleteWebhookFailure = () => {
    return {
        type: actionTypes.DELETE_WEBHOOK_FAILURE,
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

    deleteWebhookRequest,
    deleteWebhookSuccess,
    deleteWebhookFailure
};
