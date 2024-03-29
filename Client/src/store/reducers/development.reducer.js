import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';
import {deepClone} from "../../helpers";

const initialState = {webhooks: [], isLoading: false, errorMsg: null};

export const development = (state = initialState, action) => {
    switch (action.type) {

        case actionTypes.FETCH_DEV_REQUEST:
            return updateObject(state, {
                isLoading: true,
            });

        case actionTypes.FETCH_DEV_SUCCESS:
            return updateObject(state, {
                isLoading: false,
                webhooks: action.webhooks.map(webhook => ({...webhook, isLoading: false})),
            });

        case actionTypes.FETCH_DEV_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error
            });


        case actionTypes.SAVE_WEBHOOK_REQUEST:
            return updateObject(state, {
                webhooks: state.webhooks.map(webhook => ({...webhook, isLoading: action.ID === webhook.ID ? true : webhook.isLoading}))
            });

        case actionTypes.SAVE_WEBHOOK_SUCCESS:
            return updateObject(state, {
                webhooks: state.webhooks.map(webhook => ({...webhook, isLoading: action.ID === webhook.ID ? false : webhook.isLoading}))
            });

        case actionTypes.SAVE_WEBHOOK_FAILURE:
            return updateObject(state, {
                webhooks: state.webhooks.map(webhook => ({...webhook, isLoading: action.ID === webhook.ID ? false : webhook.isLoading}))
            });


        case actionTypes.DELETE_WEBHOOK_REQUEST:
            return updateObject(state, {
                webhooks: state.webhooks.map(webhook => ({...webhook, isLoading: action.ID === webhook.ID ? true : webhook.isLoading}))
            });

        case actionTypes.DELETE_WEBHOOK_SUCCESS:
            return updateObject(state, {
                webhooks: state.webhooks.filter(webhook => webhook.ID !== action.ID)
            });

        case actionTypes.DELETE_WEBHOOK_FAILURE:
            return updateObject(state, {
                errorMsg: action.error,
                webhooks: state.webhooks.map(webhook => ({...webhook, isLoading: action.ID === webhook.ID ? false : webhook.isLoading}))
            });

        case actionTypes.CREATE_WEBHOOK_REQUEST:
            return updateObject(state, {
                isLoading: true,
            });

        case actionTypes.CREATE_WEBHOOK_SUCCESS:
            return updateObject(state, {
                isLoading: false,
                errorMsg: null,
                webhooks: state.webhooks.concat([{...action.webhook, isLoading: false}])
            });

        case actionTypes.CREATE_WEBHOOK_FAILURE:
            return updateObject(state, {
                errorMsg: action.error,
                isLoading: false,
            });
        default:
            return state
    }
};