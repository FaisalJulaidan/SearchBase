import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {http} from "../../helpers";
import {assistantActions, assistantSettingsActions} from "../actions";

function* updateAssistantSettings(action) {
    try {
        const res = yield http.put(`assistant/${action.ID}`, action.updatedSettings);
        yield put(assistantSettingsActions.updateAssistantSettingsSuccess(res.data.msg));
        return yield put(assistantActions.fetchAssistants())
    } catch (error) {
        console.log(error);
        return yield put(assistantSettingsActions.updateAssistantSettingsFailure(error.response.data));
    }
}

function* watchUpdateAssistantSettings() {
    yield takeEvery(actionTypes.UPDATE_ASSISTANT_SETTINGS_REQUEST, updateAssistantSettings)
}


export function* settingsSage() {
    yield all([
        watchUpdateAssistantSettings()
    ])
}