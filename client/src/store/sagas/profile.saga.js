import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {http} from "../../helpers";
import {profileActions} from "../actions";
import {alertError, alertSuccess, destroyMessage, loadingMessage} from "../../helpers/alert";


function* getProfilePageData() {
    try {
        const res = yield http.get(`/profile`);
        return yield put(profileActions.getProfileSuccess(res.data))
    } catch (error) {
        console.log(error);
        return yield put(profileActions.getProfileFailure(error.response.data));
    }

}

function* saveProfileDetails(action) {
    try {
        loadingMessage('Saving Profile');
        const res = yield http.post(`/profile/profiledetails`, action.profileData);
        yield destroyMessage();
        yield alertSuccess('Profile saved', res.data.msg);
        yield put(profileActions.saveProfileDetailsSuccess(res.data.msg));
        return yield put(profileActions.getProfile())
    } catch (error) {
        console.log(error);
        yield destroyMessage();
        yield alertError('Error in saving Profile', error.response.data.msg);
        return yield put(profileActions.saveProfileDetailsFailure(error.response.data));
    }
}

function* saveDataSettings(action) {
    try {
        loadingMessage('Saving Data Settings');
        const res = yield http.post(`/profile/datasettings`, action.dataSettings);
        yield destroyMessage();
        yield alertSuccess('Data Settings saved', res.data.msg);
        yield put(profileActions.saveDataSettingsSuccess(res.data.msg));
        return yield put(profileActions.getProfile())
    } catch (error) {
        console.log(error);
        yield destroyMessage();
        yield alertError('Error in saving Data Settings', error.response.data.msg);
        return yield put(profileActions.saveDataSettingsFailure(error.response.data));
    }
}

function* watchProfileRequests(){
    yield takeEvery(actionTypes.GET_PROFILE_REQUEST, getProfilePageData)
}

function* watchProfileUpdates() {
    yield takeEvery(actionTypes.SAVE_PROFILE_DETAILS_REQUEST, saveProfileDetails)
}

function* watchDataSettingsUpdates() {
    yield takeEvery(actionTypes.SAVE_DATA_SETTINGS_REQUEST, saveDataSettings)
}


export function* profileSaga() {
    yield all([
        watchProfileRequests(),
        watchProfileUpdates(),
        watchDataSettingsUpdates()
    ])
}