import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {optionsActions} from "../actions";
import {http} from "../../helpers";


function* fetchOptions() {
    try {
        const res = yield http.get(`/options`);
        yield put(optionsActions.getOptionsSuccess(res.data.data));
    } catch (error) {
        console.log(error);
        return yield put(optionsActions.getOptionsFailure("Get options error"));
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