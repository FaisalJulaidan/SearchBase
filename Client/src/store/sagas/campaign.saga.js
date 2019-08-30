import {all, takeEvery, put} from 'redux-saga/effects'
import * as actionTypes from "../actions/actionTypes";
import {campaignActions} from "../actions";
import {http, errorMessage, loadingMessage, successMessage} from "helpers";


//Fetch Campaign data
function* fetchCampaignData() {
    try {
        const res = yield http.get(`/campaign_data`);
        yield put(campaignActions.fetchCampaignDataSuccess(
            res.data?.data.assistants,
            res.data?.data.crms,
            res.data?.data.databases,
            res.data?.data.messengers)
        );
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't load full assistants data";
        errorMessage(msg);
        yield put(campaignActions.fetchCampaignDataFailure(msg));
    }
}

//Fetch Candidates data
function* fetchCampaignCandidatesData() {
    try {
        const res = yield http.post(`/campaign_data`);
        yield put(campaignActions.fetchCampaignDataSuccess(
            res.data?.data.assistants,
            res.data?.data.crms,
            res.data?.data.databases,
            res.data?.data.messengers,
            res.data?.data.candidates_list)
        );
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't load full assistants data";
        errorMessage(msg);
        yield put(campaignActions.fetchCampaignDataFailure(msg));
    }
}

//Launch Campaign
function* launchCampaign({assistant_id, use_crm, crm_id, database_id, messenger_id, location, jobTitle, skills, text}) {
    try {
        loadingMessage('Launching the campaign...', 0);
        const res = yield http.post('/send_campaign',
            {assistant_id, use_crm, crm_id, database_id, messenger_id, location, jobTitle, skills, text}, {
                headers: {'Content-Type': 'application/json'},
            });
        yield put(campaignActions.launchCampaignSuccess());
        successMessage('Campaign has been launched successfully.');

    } catch (error) {
        console.log(error);
        const msg = error.response?.data?.msg || "Couldn't launch the campaign - contact support.";
        yield put(campaignActions.launchCampaignFailure(error.response.data));
        errorMessage(msg, 0);
    }
}

function* watchFetchCampaignData() {
    yield takeEvery(actionTypes.FETCH_CAMPAIGN_DATA_REQUEST, fetchCampaignData)
}

function* watchFetchCampaignCandidatesData() {
    yield takeEvery(actionTypes.FETCH_CAMPAIGN_CANDIDATES_DATA_REQUEST, fetchCampaignCandidatesData)
}

function* watchLaunchCampaign() {
    yield takeEvery(actionTypes.LAUNCH_CAMPAIGN_REQUEST, launchCampaign)
}

export function* campaignSaga() {
    yield all([
        watchFetchCampaignData(),
        watchFetchCampaignCandidatesData(),
        watchLaunchCampaign()
    ])
}