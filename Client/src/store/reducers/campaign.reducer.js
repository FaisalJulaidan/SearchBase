import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {
    assistants: [],
    crms: [],
    databases: [],
    messengers: [],
    candidates_list: [],
    isLoading: false,
    isLaunching: true,
    errorMsg: null
};

export const campaign = (state = initialState, action) => {
    switch (action.type) {

        //Fetch campaign data
        case actionTypes.FETCH_CAMPAIGN_DATA_REQUEST:
            return updateObject(state, {
                assistants: [],
                crms: [],
                databases: [],
                messengers: [],
                isLoading: true,
                errorMsg: null,
            });
        case actionTypes.FETCH_CAMPAIGN_DATA_SUCCESS:
            return updateObject(state, {
                assistants: action.assistants,
                crms: action.crms,
                databases: action.databases,
                messengers: action.messengers,
                isLoading: false,
                errorMsg: null,
            });
        case actionTypes.FETCH_CAMPAIGN_DATA_FAILURE:
            return updateObject(state, {
                assistants: [],
                crms: [],
                databases: [],
                messengers: [],
                isLoading: false,
                errorMsg: action.error
            });


        //Fetch Candidate Data
        case actionTypes.FETCH_CAMPAIGN_CANDIDATES_DATA_REQUEST:
            return updateObject(state, {
                candidates_list: [],
                isLoading: true,
                errorMsg: null,
            });
        case actionTypes.FETCH_CAMPAIGN_CANDIDATES_DATA_SUCCESS:
            return updateObject(state, {
                candidates_list: action.candidates_list,
                isLoading: false,
                errorMsg: null,
            });
        case actionTypes.FETCH_CAMPAIGN_CANDIDATES_DATA_FAILURE:
            return updateObject(state, {
                candidates_list: [],
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