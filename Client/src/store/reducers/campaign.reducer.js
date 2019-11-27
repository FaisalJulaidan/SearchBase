import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {
    campaigns: [],
    campaignOptions: null,
    campaign: null,
    isLoading: false,
    candidate_list: [],
    isCandidatesLoading: false,

    isLoadingShortlists: false,
    shortlists: [],

    isLaunchingCampaign: false,
    isSaving: false,
    isDeleting: false,
    errorMsg: null
};

export const campaign = (state = initialState, action) => {
    switch (action.type) {

        //Fetch All
        case actionTypes.FETCH_CAMPAIGNS_REQUEST:
            return updateObject(state, {
                ...initialState,
                campaigns: [],
                campaignOptions: null,
                isLoading: true,
                errorMsg: null,
            });
        case actionTypes.FETCH_CAMPAIGNS_SUCCESS:
            return updateObject(state, {
                campaigns: action.campaigns,
                campaignOptions: action.campaignOptions,
                isLoading: false,
                errorMsg: null,
            });
        case actionTypes.FETCH_CAMPAIGNS_FAILURE:
            return updateObject(state, {
                campaigns: [],
                campaignOptions: null,
                isLoading: false,
                errorMsg: action.error
            });

        //Fetch Campaign
        case actionTypes.FETCH_CAMPAIGN_REQUEST:
            return updateObject(state, {
                campaign: null,
                campaignOptions: null,
                isLoading: true,
                errorMsg: null,
            });
        case actionTypes.FETCH_CAMPAIGN_SUCCESS:
            return updateObject(state, {
                campaign: action.campaign,
                campaignOptions: action.campaignOptions,
                isLoading: false,
                errorMsg: null,
            });
        case actionTypes.FETCH_CAMPAIGN_FAILURE:
            return updateObject(state, {
                campaign: null,
                campaignOptions: null,
                isLoading: false,
                errorMsg: action.error
            });


        //Save Campaign
        case actionTypes.SAVE_CAMPAIGN_REQUEST:
            return updateObject(state, {
                campaign: null,
                isSaving: true,
                errorMsg: null,
            });
        case actionTypes.SAVE_CAMPAIGN_SUCCESS:
            return updateObject(state, {
                campaign: action.campaign,
                isSaving: false,
                errorMsg: null,
            });
        case actionTypes.SAVE_CAMPAIGN_FAILURE:
            return updateObject(state, {
                campaign: null,
                isSaving: false,
                errorMsg: action.error
            });


        //Update Campaign
        case actionTypes.UPDATE_CAMPAIGN_REQUEST:
            return updateObject(state, {
                isSaving: true,
                errorMsg: null,
            });
        case actionTypes.UPDATE_CAMPAIGN_SUCCESS:
            return updateObject(state, {
                isSaving: false,
                errorMsg: null,
            });
        case actionTypes.UPDATE_CAMPAIGN_FAILURE:
            return updateObject(state, {
                isSaving: false,
                errorMsg: action.error
            });


        //Delete Campaign
        case actionTypes.DELETE_CAMPAIGN_REQUEST:
            return updateObject(state, {
                isDeleting: true,
                errorMsg: null,
            });
        case actionTypes.DELETE_CAMPAIGN_SUCCESS:
            return updateObject(state, {
                campaigns: [...state.campaigns].filter(campaign => campaign.ID !== action.campaignID),
                isDeleting: false,
                errorMsg: null,
            });
        case actionTypes.DELETE_CAMPAIGN_FAILURE:
            return updateObject(state, {
                isDeleting: false,
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

        //Fetch JobScience shortlists
        case actionTypes.FETCH_CAMPAIGN_SHORTLISTS:
            return updateObject(state, {
                shortlists: [],
                isLoadingShortlists: true,
                errorMsg: null,
            });
        case actionTypes.FETCH_CAMPAIGN_SHORTLISTS_SUCCESS:
            return updateObject(state, {
                shortlists: Array.isArray(action.shortlists) ? action.shortlists : [],
                isLoadingShortlists: false,
                errorMsg: null,
            });
        case actionTypes.FETCH_CAMPAIGN_SHORTLISTS_FAILURE:
            return updateObject(state, {
                shortlists: [],
                isLoadingShortlists: false,
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