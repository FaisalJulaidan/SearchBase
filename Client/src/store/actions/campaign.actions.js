import * as actionTypes from './actionTypes';


// Fetch All
const fetchCampaigns = () => ({
    type: actionTypes.FETCH_CAMPAIGNS_REQUEST
});

const fetchCampaignsSuccess = (campaigns, campaignOptions) => ({
    type: actionTypes.FETCH_CAMPAIGNS_SUCCESS,
    campaigns,
    campaignOptions
});

const fetchCampaignsFailure = (errorMsg) => ({
    type: actionTypes.FETCH_CAMPAIGNS_FAILURE,
    errorMsg
});


// Fetch Campaign
const fetchCampaign = (campaignID) => ({
    type: actionTypes.FETCH_CAMPAIGN_REQUEST,
    meta: {thunk: true},
    campaignID
});

const fetchCampaignSuccess = (campaign, campaignOptions) => ({
    type: actionTypes.FETCH_CAMPAIGN_SUCCESS,
    campaign,
    campaignOptions
});

const fetchCampaignFailure = (error) => ({
    type: actionTypes.FETCH_CAMPAIGN_FAILURE,
    error
});

// Save Campaign
const saveCampaign = (name, assistant_id, use_crm, crm_id, database_id, messenger_id, location, jobTitle, skills, message) => ({
    type: actionTypes.SAVE_CAMPAIGN_REQUEST,
    meta: {thunk: true},
    name,
    assistant_id,
    use_crm,
    crm_id,
    database_id,
    messenger_id,
    location,
    jobTitle,
    skills,
    message
});

const saveCampaignSuccess = (campaign) => ({
    type: actionTypes.SAVE_CAMPAIGN_SUCCESS,
    campaign
});

const saveCampaignFailure = (error) => ({
    type: actionTypes.SAVE_CAMPAIGN_FAILURE,
    error
});


// Update Campaign
const updateCampaign = (campaignID, name, assistant_id, use_crm, crm_id, database_id, messenger_id, location, jobTitle, skills, message) => ({
    type: actionTypes.UPDATE_CAMPAIGN_REQUEST,
    campaignID,
    name,
    assistant_id,
    use_crm,
    crm_id,
    database_id,
    messenger_id,
    location,
    jobTitle,
    skills,
    message
});

const updateCampaignSuccess = () => ({
    type: actionTypes.UPDATE_CAMPAIGN_SUCCESS,
});

const updateCampaignFailure = (error) => ({
    type: actionTypes.UPDATE_CAMPAIGN_FAILURE,
    error
});


// Delete Campaign
const deleteCampaign = (campaignID) => ({
    type: actionTypes.DELETE_CAMPAIGN_REQUEST,
    meta: {thunk: true},
    campaignID
});

const deleteCampaignSuccess = (campaignID) => ({
    type: actionTypes.DELETE_CAMPAIGN_SUCCESS,
    campaignID
});

const deleteCampaignFailure = (error) => ({
    type: actionTypes.DELETE_CAMPAIGN_FAILURE,
    error
});

// Fetch Candidates List
const fetchCampaignCandidatesData = (assistant_id, use_crm, crm_id, database_id, messenger_id, location, jobTitle, skills, text, outreach_type, email_title) => ({
    type: actionTypes.FETCH_CAMPAIGN_CANDIDATES_DATA_REQUEST,
    assistant_id,
    use_crm,
    crm_id,
    database_id,
    messenger_id,
    location,
    jobTitle,
    skills,
    text,
    outreach_type,
    email_title
});

const fetchCampaignCandidatesDataSuccess = (candidate_list) => ({
    type: actionTypes.FETCH_CAMPAIGN_CANDIDATES_DATA_SUCCESS,
    candidate_list
});

const fetchCampaignCandidatesDataFailure = (error) => ({
    type: actionTypes.FETCH_CAMPAIGN_CANDIDATES_DATA_FAILURE,
    error
});


// Launch Campaign
const launchCampaign = (assistant_id, use_crm, crm_id, database_id, messenger_id, location, jobTitle, skills, text, candidate_list, outreach_type, email_title) => ({
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
    candidate_list,
    outreach_type,
    email_title
});

const launchCampaignSuccess = () => ({
    type: actionTypes.LAUNCH_CAMPAIGN_SUCCESS,
});

const launchCampaignFailure = (errorMsg) => ({
    type: actionTypes.LAUNCH_CAMPAIGN_FAILURE,
    errorMsg
});


export const campaignActions = {
    fetchCampaigns,
    fetchCampaignsSuccess,
    fetchCampaignsFailure,

    fetchCampaign,
    fetchCampaignSuccess,
    fetchCampaignFailure,

    saveCampaign,
    saveCampaignSuccess,
    saveCampaignFailure,

    updateCampaign,
    updateCampaignSuccess,
    updateCampaignFailure,

    deleteCampaign,
    deleteCampaignSuccess,
    deleteCampaignFailure,

    fetchCampaignCandidatesData,
    fetchCampaignCandidatesDataSuccess,
    fetchCampaignCandidatesDataFailure,

    launchCampaign,
    launchCampaignSuccess,
    launchCampaignFailure
};