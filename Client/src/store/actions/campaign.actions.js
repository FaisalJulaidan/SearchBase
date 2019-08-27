import * as actionTypes from './actionTypes';

const fetchCampaignData = () => ({
    type: actionTypes.FETCH_CAMPAIGN_DATA_REQUEST
});

const fetchCampaignDataSuccess = (assistants, database) => ({
    type: actionTypes.FETCH_CAMPAIGN_DATA_SUCCESS,
    assistants,
    database
});

const fetchCampaignDataFailure = (error) => ({
    type: actionTypes.FETCH_CAMPAIGN_DATA_FAILURE,
    error
});


const launchCampaign = (assistant_id, use_crm, database_id, location, jobTitle, skills, text) => ({
    type: actionTypes.LAUNCH_CAMPAIGN_REQUEST,
    assistant_id,
    use_crm,
    database_id,
    location,
    jobTitle,
    skills,
    text
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
    launchCampaign,
    launchCampaignSuccess,
    launchCampaignFailure
};