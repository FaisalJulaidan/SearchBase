// import {put, takeEvery, all} from 'redux-saga/effects'
// import * as actionTypes from '../actions/actionTypes';
// import {http} from "../../helpers";
// import {profileActions} from "../actions";
//
// function* saveProfileDetails(action) {
//     try {
//         const res = yield http.put(`/admin/profile/profiledetails`, action.profile);
//         yield put(assistantSettingsActions.updateAssistantSettingsSuccess(res.data.msg));
//         return yield put(assistantActions.fetchAssistants())
//     } catch (error) {
//         console.log(error);
//         return yield put(assistantSettingsActions.updateAssistantSettingsFailure(error.response.data));
//     }
// }
//
// function* watchUpdateAssistantSettings() {
//     yield takeEvery(actionTypes.UPDATE_ASSISTANT_SETTINGS_REQUEST, updateAssistantSettings)
// }
//
//
// export function* settingsSage() {
//     yield all([
//         watchUpdateAssistantSettings()
//     ])
// }