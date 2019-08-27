import * as actionTypes from './actionTypes';

// Fetch All
const launchCampaign = (crmType,jobTitle,skills,location) => ({
    type: actionTypes.LAUNCH_CAMPAIGN_REQUEST,
    crmType,
    jobTitle,
    skills,
    location
});

const launchCampaignSuccess = () => ({
    type: actionTypes.LAUNCH_CAMPAIGN_SUCCESS,
});

const launchCampaignFailure = (errorMsg) => ({
    type: actionTypes.LAUNCH_CAMPAIGN_FAILURE,
    errorMsg
});

export const campaignActions = {
    launchCampaign,
    launchCampaignSuccess,
    launchCampaignFailure
};