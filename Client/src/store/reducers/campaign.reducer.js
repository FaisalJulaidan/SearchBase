import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {fullAssistantList: [], isLoading: false, isLaunching: true, errorMsg: null};

export const campaign = (state = initialState, action) => {
    switch (action.type) {

        //FETCH ASSISTANTS DATA
        case actionTypes.FETCH_FULL_ASSISTANTS_REQUEST:
            return updateObject(state, {
                fullAssistantList: [],
                isLoading: true,
                errorMsg: null,
            });
        case actionTypes.FETCH_FULL_ASSISTANTS_SUCCESS:
            return updateObject(state, {
                fullAssistantList: action.fullAssistantList,
                isLoading: false,
                errorMsg: null,
            });
        case actionTypes.FETCH_FULL_ASSISTANTS_FAILURE:
            return updateObject(state, {
                fullAssistantList: [],
                isLoading: false,
                errorMsg: action.error
            });

        //Launch Campaign
        case actionTypes.LAUNCH_CAMPAIGN_REQUEST:
            return updateObject(state, {
                isLaunching: true,
                errorMsg: null,
            });
        case actionTypes.LAUNCH_CAMPAIGN_SUCCESS:
            return updateObject(state, {
                isLaunching: false,
            });
        case actionTypes.LAUNCH_CAMPAIGN_FAILURE:
            return updateObject(state, {
                isLaunching: false,
                errorMsg: action.error
            });
        default:
            return state;
    }
};