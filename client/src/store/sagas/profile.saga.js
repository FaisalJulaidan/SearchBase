import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {http, updateUsername} from "../../helpers";
import {profileActions} from "../actions";
import {alertError, alertSuccess, destroyMessage, loadingMessage, errorMessage, sucessMessage} from "../../helpers/alert";



function* getProfileData() {
    try {
        const res = yield http.get(`/profile`);
        const profile = res.data.data;
        // Update username in localStorage
        yield updateUsername(profile.user.Firstname, profile.user.Surname);
        return yield put(profileActions.getProfileSuccess(profile))

    } catch (error) {
        console.log(error);
        return yield put(profileActions.getProfileFailure(error.response.data));
    }

}

function* saveProfileData(action) {
    try {
        loadingMessage('Saving profile...', 0);
        const res = yield http.post(`/profile`, action.profileData);
        yield put(profileActions.saveProfileDetailsSuccess(res.data.msg));
        yield destroyMessage();
        yield sucessMessage('Profile saved');

        return yield put(profileActions.getProfile())
    } catch (error) {
        console.log(error);
        yield destroyMessage();
        yield errorMessage(error.response.data.msg);
        return yield put(profileActions.saveProfileDetailsFailure(error.response.data));
    }
}

function* saveDataSettings(action) {
    try {
        loadingMessage('Saving Data Settings...', 0);
        const res = yield http.post(`/profile/settings`, action.dataSettings);
        yield destroyMessage();
        yield put(profileActions.saveDataSettingsSuccess(res.data.msg));
        yield sucessMessage('Data Settings saved');
        return yield put(profileActions.getProfile())
    } catch (error) {
        console.log(error);
        yield destroyMessage();
        yield errorMessage(error.response.data.msg);
        return yield put(profileActions.saveDataSettingsFailure(error.response.data));
    }
}

function* changePassword({newPassword, oldPassword}) {
    try {
        loadingMessage('Updating passwords...', 0);
        const res = yield http.post(`/profile/password`, {newPassword, oldPassword});
        yield destroyMessage();
        yield put(profileActions.changePasswordSuccess(res.data.msg));
        yield sucessMessage('Password updated');

    } catch (error) {
        console.log(error);
        yield destroyMessage();
        yield errorMessage(error.response.data.msg);
        return yield put(profileActions.changePasswordFailure(error.response.data));
    }
}


function* watchProfileRequests(){
    yield takeEvery(actionTypes.GET_PROFILE_REQUEST, getProfileData)
}

function* watchProfileUpdates() {
    yield takeEvery(actionTypes.SAVE_PROFILE_DETAILS_REQUEST, saveProfileData)
}

function* watchDataSettingsUpdates() {
    yield takeEvery(actionTypes.SAVE_DATA_SETTINGS_REQUEST, saveDataSettings)
}

function* watchChangePassword(){
    yield takeEvery(actionTypes.CHANGE_PASS_REQUEST, changePassword)
}

export function* profileSaga() {
    yield all([
        watchProfileRequests(),
        watchProfileUpdates(),
        watchDataSettingsUpdates(),
        watchChangePassword(),
    ])
}