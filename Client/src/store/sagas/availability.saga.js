import {all, put, takeEvery, takeLatest} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import { availabilityActions } from '../actions';
import {errorMessage, flow, http, loadingMessage, successMessage} from "helpers";

function* fetchAvailability() {
    try {
        const res = yield http.get(`/candidate/availability`);
        yield put(availabilityActions.fetchAvailabilitySuccess(res.data?.data.availability));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't load candidate availability";
        errorMessage(msg);
        yield put(availabilityActions.fetchAvailabilityFailure(msg));
    }
}

function* watchFetchAvailability() {
    yield takeEvery(actionTypes.FETCH_AVAILABILITY_REQUEST, fetchAvailability);
}




export function* availabilitySaga() {
    yield all([
        watchFetchAvailability(),
    ])
}
