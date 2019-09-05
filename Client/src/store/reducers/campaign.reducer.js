import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {
    campaignsList:[],
    assistants: [],
    crms: [],
    databases: [],
    messengers: [],
    candidate_list: [],
    isLoading: false,
    isCandidatesLoading: false,
    isLaunchingCampaign: false,
    errorMsg: null
};

export const campaign = (state = initialState, action) => {
    switch (action.type) {

        //Fetch All
        case actionTypes.FETCH_CAMPAIGNS_REQUEST:
            return updateObject(state, {
                campaignsList: [],
                isLoading: true,
                errorMsg: null,
            });
        case actionTypes.FETCH_CAMPAIGNS_SUCCESS:
            return updateObject(state, {
                campaignsList: action.campaignsList,
                isLoading: false,
                errorMsg: null,
            });
        case actionTypes.FETCH_CAMPAIGNS_FAILURE:
            return updateObject(state, {
                campaignsList: [],
                isLoading: false,
                errorMsg: action.error
            });

        //Fetch campaign
        case actionTypes.FETCH_CAMPAIGN_REQUEST:
            return updateObject(state, {
                assistants: [],
                crms: [],
                databases: [],
                messengers: [],
                isLoading: true,
                errorMsg: null,
            });
        case actionTypes.FETCH_CAMPAIGN_SUCCESS:
            return updateObject(state, {
                assistants: action.assistants,
                crms: action.crms,
                databases: action.databases,
                messengers: action.messengers,
                isLoading: false,
                errorMsg: null,
            });
        case actionTypes.FETCH_CAMPAIGN_FAILURE:
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
                candidate_list: [],
                isCandidatesLoading: true,
                errorMsg: null,
            });
        case actionTypes.FETCH_CAMPAIGN_CANDIDATES_DATA_SUCCESS:
            return updateObject(state, {
                candidate_list: action.candidate_list || [],
                isCandidatesLoading: false,
                errorMsg: null,
            });
        case actionTypes.FETCH_CAMPAIGN_CANDIDATES_DATA_FAILURE:
            return updateObject(state, {
                candidate_list: [],
                isCandidatesLoading: false,
                errorMsg: action.error
            });


        //Launch Campaign
        case actionTypes.LAUNCH_CAMPAIGN_REQUEST:
            return updateObject(state, {
                isLaunchingCampaign: true,
                errorMsg: null,
            });
        case actionTypes.LAUNCH_CAMPAIGN_SUCCESS:
            return updateObject(state, {
                isLaunchingCampaign: false,
                errorMsg: null,
            });
        case actionTypes.LAUNCH_CAMPAIGN_FAILURE:
            return updateObject(state, {
                isLaunchingCampaign: false,
                errorMsg: action.error
            });
        default:
            return state;
    }
};