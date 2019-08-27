import {all, put, takeLatest} from 'redux-saga/effects'
import {authActions} from "../actions";
import {successMessage} from "helpers";
import {errorMessage, loadingMessage} from "helpers/alert";
import axios from 'axios';

//Launch Campaign
function* launchCampaign({crmType, jobTitle, skills, location}) {
    try {
        loadingMessage('Launching the campaign...', 0);
        const res = yield axios.post(`/campaign`, {crmType, jobTitle, skills, location}, {
            headers: {'Content-Type': 'application/json'},
        });
        yield put(authActions.demoSuccess());
        successMessage('Campaign has been launched successfully.');

    } catch (error) {
        console.log(error);
        const msg = error.response?.data?.msg || "Couldn't launch the campaign - contact support.";
        yield put(authActions.demoFailure(error.response.data));
        errorMessage(msg, 0);
    }
}


export function* campaignSaga() {
    yield all([
        launchCampaign
    ])
}