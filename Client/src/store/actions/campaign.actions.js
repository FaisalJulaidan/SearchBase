import * as actionTypes from './actionTypes';

const fetchFullAssistants = () => ({
    type: actionTypes.FETCH_FULL_ASSISTANTS_REQUEST
});

const fetchFullAssistantsSuccess = (fullAssistantList) => ({
    type: actionTypes.FETCH_FULL_ASSISTANTS_SUCCESS,
    fullAssistantList
});

const fetchFullAssistantsFailure = (error) => ({
    type: actionTypes.FETCH_FULL_ASSISTANTS_FAILURE,
    error
});


const launchCampaign = (assistant_id, location, jobTitle, skills,text) => ({
    type: actionTypes.LAUNCH_CAMPAIGN_REQUEST,
    assistant_id,
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
    fetchFullAssistants,
    fetchFullAssistantsSuccess,
    fetchFullAssistantsFailure,
    launchCampaign,
    launchCampaignSuccess,
    launchCampaignFailure
};