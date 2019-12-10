import {all, takeLatest, put, takeEvery} from 'redux-saga/effects'
import * as actionTypes from "../actions/actionTypes";
import {autoPilotActions, campaignActions} from "../actions";
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
function* saveCampaign({name, assistant_id, use_crm, crm_id, useShortlist, shortlist_id, database_id, messenger_id, location, preferredJobTitle, skills, message, meta}) {
    try {
        loadingMessage('Saving campaign...', 0);
        const res = yield http.post('/campaign',
            {
                name,
                assistant_id,
                use_crm,
                crm_id,
                useShortlist,
                shortlist_id,
                database_id,
                messenger_id,
                location,
                preferredJobTitle,
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
function* updateCampaign({campaignID, name, assistant_id, use_crm, crm_id, useShortlist, shortlist_id, database_id, messenger_id, location, preferredJobTitle, skills, message}) {
    try {
        loadingMessage('Updating campaign...', 0);
        const res = yield http.post(`/campaign/${campaignID}`,
            {
                name,
                assistant_id,
                use_crm,
                crm_id,
                useShortlist,
                shortlist_id,
                database_id,
                messenger_id,
                location,
                preferredJobTitle,
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
function* fetchCampaignCandidatesData({assistant_id, use_crm, crm_id, useShortlist, shortlist_id, database_id, messenger_id, location, preferredJobTitle, jobType, skills, text, outreach_type, email_title, perfect_match}) {
    try {
        const res = yield http.post('/campaign/action',
            {
                assistant_id,
                use_crm,
                crm_id,
                useShortlist,
                shortlist_id,
                database_id,
                messenger_id,
                location,
                preferredJobTitle,
                jobType,
                skills,
                text,
                outreach_type,
                email_title,
                perfect_match
            }, {
                timeout: 600000,
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

//Fetch JobScience shortlists
function* fetchShortlists({crm_id}) {
    try {
        const res = yield http.get(`/campaign/candidate_lists/${crm_id}`);
        yield put(campaignActions.fetchShortlistsSuccess(
            res.data?.data?.data)
        );
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't load shortlists";
        errorMessage(msg);
        yield put(campaignActions.fetchShortlistsFailure(msg));
    }
}

//Launch Campaign
function* launchCampaign({assistant_id, use_crm, crm_id, useShortlist, shortlist_id, database_id, messenger_id, location, preferredJobTitle, jobType, skills, text, candidate_list, outreach_type, email_title, perfect_match}) {
    try {
        loadingMessage('Launching the campaign...', 0);
        const res = yield http.put('/campaign/action',
            {
                assistant_id,
                use_crm,
                crm_id,
                useShortlist,
                shortlist_id,
                database_id,
                messenger_id,
                location,
                preferredJobTitle,
                jobType,
                skills,
                text,
                candidate_list,
                outreach_type,
                email_title,
                perfect_match
            }, {
                timeout: 600000,
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

//Update Campaign status
function* updateStatus({status, campaignID}) {
    try {
        loadingMessage('Updating Status', 0);
        const res = yield http.put(`/campaign/${campaignID}/status`, {status});
        yield put(campaignActions.updateStatusSuccess('Status updated successfully', status, campaignID));
        successMessage('Status updated');

    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't update campaign's status";
        yield put(campaignActions.updateStatusFailure(msg));
        errorMessage(msg);
    }
}

function* watchFetchCampaigns() {
    yield takeLatest(actionTypes.FETCH_CAMPAIGNS_REQUEST, fetchCampaigns)
}

function* watchSaveCampaign() {
    yield takeLatest(actionTypes.SAVE_CAMPAIGN_REQUEST, saveCampaign)
}

function* watchUpdateCampaign() {
    yield takeLatest(actionTypes.UPDATE_CAMPAIGN_REQUEST, updateCampaign)
}

function* watchDeleteCampaign() {
    yield takeLatest(actionTypes.DELETE_CAMPAIGN_REQUEST, deleteCampaign)
}

function* watchFetchCampaign() {
    yield takeLatest(actionTypes.FETCH_CAMPAIGN_REQUEST, fetchCampaign)
}

function* watchFetchCampaignCandidatesData() {
    yield takeLatest(actionTypes.FETCH_CAMPAIGN_CANDIDATES_DATA_REQUEST, fetchCampaignCandidatesData)
}

function* watchFetchShortlists() {
    yield takeLatest(actionTypes.FETCH_CAMPAIGN_SHORTLISTS, fetchShortlists)
}

function* watchLaunchCampaign() {
    yield takeLatest(actionTypes.LAUNCH_CAMPAIGN_REQUEST, launchCampaign)
}

function* watchUpdateStatus() {
    yield takeLatest(actionTypes.UPDATE_CAMPAIGN_STATUS_REQUEST, updateStatus)
}

export function* campaignSaga() {
    yield all([
        watchFetchCampaigns(),
        watchFetchCampaign(),
        watchSaveCampaign(),
        watchUpdateCampaign(),
        watchDeleteCampaign(),
        watchFetchCampaignCandidatesData(),
        watchFetchShortlists(),
        watchLaunchCampaign(),
        watchUpdateStatus(),
    ])
}