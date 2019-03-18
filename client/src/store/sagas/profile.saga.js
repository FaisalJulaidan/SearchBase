import {put, takeLatest, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {http, updateUsername} from "../../helpers";
import {profileActions} from "../actions";
import {loadingMessage, errorMessage, successMessage} from "../../helpers/alert";



function* getProfileData() {
    try {
        const res = yield http.get(`/profile`);
        const profile = yield res.data?.data;

        // Update username in localStorage
        yield updateUsername(profile.user.Firstname, profile.user.Surname);
        yield put(profileActions.getProfileSuccess(profile))

    } catch (error) {
        console.log(error);
        const msg = "Couldn't load profile";
        yield put(profileActions.getProfileFailure(msg));
        errorMessage(msg);
    }

}

function* saveProfileData(action) {
    try {
        loadingMessage('Saving profile...', 0);
        const res = yield http.post(`/profile`, action.profileData);
        yield put(profileActions.saveProfileDetailsSuccess(res.data.msg));
        yield put(profileActions.getProfile());
        successMessage('Profile saved');

    } catch (error) {
        console.log(error);
        const msg = "Couldn't save profile";
        yield put(profileActions.saveProfileDetailsFailure(msg));
        errorMessage(msg);
    }
}

function* saveDataSettings(action) {
    try {
        loadingMessage('Saving Data Settings...', 0);
        const res = yield http.post(`/profile/settings`, action.dataSettings);
        yield put(profileActions.saveDataSettingsSuccess(res.data.msg));
        yield put(profileActions.getProfile());
        successMessage('Data Settings saved');
    } catch (error) {
        console.log(error);
        const msg = "Couldn't save settings";
        yield put(profileActions.saveDataSettingsFailure(msg));
        errorMessage(msg);
    }
}

function* changePassword({newPassword, oldPassword}) {
    try {
        loadingMessage('Updating passwords...', 0);
        const res = yield http.post(`/profile/password`, {newPassword, oldPassword});
        yield put(profileActions.changePasswordSuccess(res.data.msg));
        successMessage('Password updated');

    } catch (error) {
        console.log(error);
        const msg = "Couldn't update password";
        yield put(profileActions.changePasswordFailure(msg));
        errorMessage(msg);
    }
}


function* watchProfileRequests(){
    yield takeLatest(actionTypes.GET_PROFILE_REQUEST, getProfileData)
}

function* watchProfileUpdates() {
    yield takeLatest(actionTypes.SAVE_PROFILE_DETAILS_REQUEST, saveProfileData)
}

function* watchDataSettingsUpdates() {
    yield takeLatest(actionTypes.SAVE_DATA_SETTINGS_REQUEST, saveDataSettings)
}

function* watchChangePassword(){
    yield takeLatest(actionTypes.CHANGE_PASS_REQUEST, changePassword)
}

export function* profileSaga() {
    yield all([
        watchProfileRequests(),
        watchProfileUpdates(),
        watchDataSettingsUpdates(),
        watchChangePassword(),
    ])
}