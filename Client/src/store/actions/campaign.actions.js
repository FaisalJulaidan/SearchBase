import * as actionTypes from './actionTypes';

const fetchCampaignData = () => ({
    type: actionTypes.FETCH_CAMPAIGN_DATA_REQUEST
});

const fetchCampaignDataSuccess = (assistants, crms, databases, messengers) => ({
    type: actionTypes.FETCH_CAMPAIGN_DATA_SUCCESS,
    assistants,
    crms,
    databases,
    messengers
});

const fetchCampaignDataFailure = (error) => ({
    type: actionTypes.FETCH_CAMPAIGN_DATA_FAILURE,
    error
});

const fetchCampaignCandidatesData = (assistant_id, use_crm, crm_id, database_id, messenger_id, location, jobTitle, skills, text) => ({
    type: actionTypes.FETCH_CAMPAIGN_CANDIDATES_DATA_REQUEST,
    assistant_id,
    use_crm,
    crm_id,
    database_id,
    messenger_id,
    location,
    jobTitle,
    skills,
    text
});

const fetchCampaignCandidatesDataSuccess = (candidate_list) => ({
    type: actionTypes.FETCH_CAMPAIGN_CANDIDATES_DATA_SUCCESS,
    candidate_list
});

const fetchCampaignCandidatesDataFailure = (error) => ({
    type: actionTypes.FETCH_CAMPAIGN_CANDIDATES_DATA_FAILURE,
    error
});


const launchCampaign = (assistant_id, use_crm, crm_id, database_id, messenger_id, location, jobTitle, skills, text,candidate_list) => ({
    type: actionTypes.LAUNCH_CAMPAIGN_REQUEST,
    assistant_id,
    use_crm,
    crm_id,
    database_id,
    messenger_id,
    location,
    jobTitle,
    skills,
    text,
    candidate_list
});

const launchCampaignSuccess = () => ({
    type: actionTypes.LAUNCH_CAMPAIGN_SUCCESS,
});

const launchCampaignFailure = (errorMsg) => ({
    type: actionTypes.LAUNCH_CAMPAIGN_FAILURE,
    errorMsg
});

export const campaignActions = {
    fetchCampaignData,
    fetchCampaignDataSuccess,
    fetchCampaignDataFailure,

    fetchCampaignCandidatesData,
    fetchCampaignCandidatesDataSuccess,
    fetchCampaignCandidatesDataFailure,

    launchCampaign,
    launchCampaignSuccess,
    launchCampaignFailure
};