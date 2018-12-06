import {delay} from 'redux-saga'
import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {flowActions} from "../actions/flow.actions";
import {http} from "../../helpers";
import {assistantActions, settingsActions} from "../actions";

function* updateSettings(action) {
    try {
        const res = yield http.put(`assistant/${action.ID}`, action.updatedSettings);
        yield put(settingsActions.updateSettingsSuccess(res.data.msg));
        return yield put(assistantActions.fetchAssistants())
    } catch (error) {
        console.log(error);
        return yield put(settingsActions.updateSettingsFailure(error.response.data));
    }
}

function* watchUpdateSettings() {
    yield takeEvery(actionTypes.UPDATE_SETTINGS_REQUEST, updateSettings)
}


export function* settingsSage() {
    yield all([
        watchUpdateSettings()
    ])
}