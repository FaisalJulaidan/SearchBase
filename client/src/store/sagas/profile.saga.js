import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {http} from "../../helpers";
import {profileActions} from "../actions";

function* saveProfileDetails(action) {
    try {
        const res = yield http.put(`/admin/profile/profiledetails`, action.profileData);
        yield put(profileActions.saveProfileDetailsSuccess(res.data.msg));
        return yield put(assistantActions.fetchAssistants())
    } catch (error) {
        console.log(error);
        return yield put(profileActions.saveProfileDetailsFailure(error.response.data));
    }
}

function* saveDataSettings(action) {
    try {
        const res = yield http.put(`/admin/profile/datasettings`, action.dataSettings);
        yield put(profileActions.saveProfileDetailsSuccess(res.data.msg));
        return yield put(assistantActions.fetchAssistants())
    } catch (error) {
        console.log(error);
        return yield put(profileActions.saveProfileDetailsFailure(error.response.data));
    }
}

function* watchProfilePageUpdates() {
    yield takeEvery(actionTypes.SAVE_PROFILE_DETAILS_REQUEST, saveProfileDetails)
    yield takeEvery(actionTypes.SAVE_DATA_SETTINGS_REQUEST, saveDataSettings)
}


export function* settingsSage() {
    yield all([
        watchProfilePageUpdates()
    ])
}