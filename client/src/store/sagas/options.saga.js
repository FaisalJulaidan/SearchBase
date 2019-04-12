import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {optionsActions} from "../actions";
import {warningMessage, http} from "helpers";


function* fetchOptions() {
    try {
        const res = yield http.get(`/options`);
        yield put(optionsActions.getOptionsSuccess(res.data.data));
    } catch (error) {
        console.log(error);
        const msg = "Couldn't load dashboard options";
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