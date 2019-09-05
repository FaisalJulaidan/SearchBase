import {all, takeEvery, put} from 'redux-saga/effects'
import * as actionTypes from "../actions/actionTypes";
import {campaignActions} from "../actions";
import {http, errorMessage, loadingMessage, successMessage} from "helpers";

//Fetch All
function* fetchCampaigns() {
    try {
        const res = yield http.get(`/campaigns_data`);
        yield put(campaignActions.fetchCampaignsSuccess(
            res.data?.data.campaignsList)
        );
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't load campaigns";
        errorMessage(msg);
        yield put(campaignActions.fetchCampaignsFailure(msg));
    }
}

//Fetch Campaign
function* fetchCampaign() {
    try {
        const res = yield http.get(`/campaign_data`);
        yield put(campaignActions.fetchCampaignSuccess(
            res.data?.data.assistants,
            res.data?.data.crms,
            res.data?.data.databases,
            res.data?.data.messengers)
        );
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't load campaign data";
        errorMessage(msg);
        yield put(campaignActions.fetchCampaignFailure(msg));
    }
}

//Fetch Candidates data
function* fetchCampaignCandidatesData({assistant_id, use_crm, crm_id, database_id, messenger_id, location, jobTitle, skills, text}) {
    try {
        const res = yield http.post('/campaign_data',
            {assistant_id, use_crm, crm_id, database_id, messenger_id, location, jobTitle, skills, text}, {
                headers: {'Content-Type': 'application/json'},
            });
        yield put(campaignActions.fetchCampaignCandidatesDataSuccess(
            res.data?.data.candidate_list
        ));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't load candidates data";
        errorMessage(msg);
        yield put(campaignActions.fetchCampaignCandidatesDataFailure(msg));
    }
}

//Launch Campaign
function* launchCampaign({assistant_id, use_crm, crm_id, database_id, messenger_id, location, jobTitle, skills, text, candidate_list}) {
    try {
        loadingMessage('Launching the campaign...', 0);
        const res = yield http.post('/send_campaign',
            {
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
            }, {
                headers: {'Content-Type': 'application/json'},
            });
        yield put(campaignActions.launchCampaignSuccess());
        successMessage('Campaign has been launched successfully.');

    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't launch the campaign - contact support.";
        yield put(campaignActions.launchCampaignFailure(error.response.data));
        errorMessage(msg, 0);
    }
}

function* watchFetchCampaigns() {
    yield takeEvery(actionTypes.FETCH_CAMPAIGNS_REQUEST, fetchCampaigns)
}

function* watchFetchCampaign() {
    yield takeEvery(actionTypes.FETCH_CAMPAIGN_REQUEST, fetchCampaign)
}

function* watchFetchCampaignCandidatesData() {
    yield takeEvery(actionTypes.FETCH_CAMPAIGN_CANDIDATES_DATA_REQUEST, fetchCampaignCandidatesData)
}

function* watchLaunchCampaign() {
    yield takeEvery(actionTypes.LAUNCH_CAMPAIGN_REQUEST, launchCampaign)
}

export function* campaignSaga() {
    yield all([
        watchFetchCampaigns(),
        watchFetchCampaign(),
        watchFetchCampaignCandidatesData(),
        watchLaunchCampaign()
    ])
}