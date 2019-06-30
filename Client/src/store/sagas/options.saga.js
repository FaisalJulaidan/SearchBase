import {all, put, takeEvery} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {optionsActions} from "../actions";
import {http, warningMessage} from "helpers";


function* fetchOptions() {
    try {
        const res = yield http.get(`/options`);
        yield put(optionsActions.getOptionsSuccess(res.data.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't load dashboard options";
        yield put(optionsActions.getOptionsFailure(msg));
        warningMessage("Server has been updated, login again please to avoid errors!", 0);
    }
}

function* watchFetchOptions() {
    yield takeEvery(actionTypes.FETCH_OPTIONS_REQUEST, fetchOptions)
}


export function* optionsSaga() {
    yield all([
        watchFetchOptions(),
    ])
}
