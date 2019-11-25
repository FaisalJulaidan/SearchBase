import {all, takeEvery, put} from 'redux-saga/effects'
import * as actionTypes from "../actions/actionTypes";
import {campaignActions} from "../actions";
import {http, errorMessage, loadingMessage, successMessage} from "helpers";

//Fetch All
function* fetchCampaigns() {
    try {
        const res = yield http.get(`/campaign/action`);
        yield put(campaignActions.fetchCampaignsSuccess(
            res.data?.data.campaigns, res.data?.data.campaignOptions)
        );
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't load campaigns";
        errorMessage(msg);
        yield put(campaignActions.fetchCampaignsFailure(msg));
    }
}

//Fetch Campaign
function* fetchCampaign({campaignID, meta}) {
    try {
        const res = yield http.get(`/campaign/${campaignID}`);
        yield put({
            ...campaignActions.fetchCampaignSuccess(res.data?.data.campaign, res.data?.data.campaignOptions),
            meta
        });
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't load campaigns";
        errorMessage(msg);
        yield put({...campaignActions.fetchCampaignFailure(msg), meta});
    }
}

//Save Campaign
function* saveCampaign({name, assistant_id, use_crm, crm_id, shortlist, database_id, messenger_id, location, jobTitle, skills, message, meta}) {
    try {
        loadingMessage('Saving campaign...', 0);
        const res = yield http.post('/campaign',
            {
                name,
                assistant_id,
                use_crm,
                crm_id,
                shortlist,
                database_id,
                messenger_id,
                location,
                jobTitle,
                skills,
                message
            }, {
                headers: {'Content-Type': 'application/json'},
            });
        yield put({
            ...campaignActions.saveCampaignSuccess(
                res.data?.data.campaign
            ), meta
        });
        successMessage("Campaign saved successfully.");
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't Save Campaign.";
        errorMessage(msg);
        yield put(campaignActions.saveCampaignFailure(msg));
    }
}

//update Campaign
function* updateCampaign({campaignID, name, assistant_id, use_crm, crm_id, shortlist, database_id, messenger_id, location, jobTitle, skills, message}) {
    try {
        loadingMessage('Updating campaign...', 0);
        const res = yield http.post(`/campaign/${campaignID}`,
            {
                name,
                assistant_id,
                use_crm,
                crm_id,
                shortlist,
                database_id,
                messenger_id,
                location,
                jobTitle,
                skills,
                message
            }, {
                headers: {'Content-Type': 'application/json'},
            });
        yield put(campaignActions.updateCampaignSuccess());
        successMessage("Campaign updated.");
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't update campaign.";
        errorMessage(msg);
        yield put(campaignActions.updateCampaignFailure(msg));
    }
}

//update Campaign
function* deleteCampaign({campaignID, meta}) {
    try {
        loadingMessage('Deleting campaign...', 0);
        const res = yield http.delete(`/campaign/${campaignID}`);
        yield put({...campaignActions.deleteCampaignSuccess(campaignID), meta});
        successMessage("Campaign deleted.");
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't delete campaign.";
        errorMessage(msg);
        yield put(campaignActions.deleteCampaignFailure(msg));
    }
}

//Fetch Candidates data
function* fetchCampaignCandidatesData({assistant_id, use_crm, crm_id, shortlist, database_id, messenger_id, location, jobTitle, jobType, skills, text, outreach_type, email_title}) {
    try {
        const res = yield http.post('/campaign/action',
            {
                assistant_id,
                use_crm,
                crm_id,
                shortlist,
                database_id,
                messenger_id,
                location,
                jobTitle,
                jobType,
                skills,
                text,
                outreach_type,
                email_title
            }, {
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
function* launchCampaign({assistant_id, use_crm, crm_id, shortlist, database_id, messenger_id, location, jobTitle, jobType, skills, text, candidate_list, outreach_type, email_title}) {
    try {
        loadingMessage('Launching the campaign...', 0);
        const res = yield http.put('/campaign/action',
            {
                assistant_id,
                use_crm,
                crm_id,
                shortlist,
                database_id,
                messenger_id,
                location,
                jobTitle,
                jobType,
                skills,
                text,
                candidate_list,
                outreach_type,
                email_title
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

function* watchSaveCampaign() {
    yield takeEvery(actionTypes.SAVE_CAMPAIGN_REQUEST, saveCampaign)
}

function* watchUpdateCampaign() {
    yield takeEvery(actionTypes.UPDATE_CAMPAIGN_REQUEST, updateCampaign)
}

function* watchDeleteCampaign() {
    yield takeEvery(actionTypes.DELETE_CAMPAIGN_REQUEST, deleteCampaign)
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
        watchSaveCampaign(),
        watchUpdateCampaign(),
        watchDeleteCampaign(),
        watchFetchCampaignCandidatesData(),
        watchLaunchCampaign()
    ])
}