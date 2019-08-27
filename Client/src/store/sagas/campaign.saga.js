import {all, put} from 'redux-saga/effects'
import {campaignActions} from "../actions";
import {http,errorMessage, loadingMessage,successMessage} from "helpers";
import axios from 'axios';


//Fetch Assistant data
function* fetchFullAssistants() {
    try {
        const res = yield http.get(`/full_assistants`);
        yield put(campaignActions.fetchFullAssistantsSuccess(res.data?.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't load full assistants data";
        errorMessage(msg);
        yield put(campaignActions.fetchFullAssistantsFailure(msg));
    }
}

//Launch Campaign
function* launchCampaign({assistant_id, location, jobTitle, skills,text}) {
    try {
        loadingMessage('Launching the campaign...', 0);
        const res = yield axios.post(`/send_campaign`, {assistant_id, location, jobTitle, skills,text}, {
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


export function* campaignSaga() {
    yield all([
        fetchFullAssistants,
        launchCampaign
    ])
}