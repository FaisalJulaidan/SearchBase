import {all, put, takeEvery} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {appointmentActions} from "../actions";
import {errorMessage, http} from "helpers";

// import * as Sentry from '@sentry/browser';

function* fetchAppointments({assistantID}) {
    try {
        const res = yield http.get(`/appointments`);
        yield put(appointmentActions.fetchAppointmentsSuccess(res.data?.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't fetch appointments";
        yield put(appointmentActions.fetchAppointmentsFailure(msg));
        errorMessage(msg);
    }
}

function* watchfetchAppointments() {
    yield takeEvery(actionTypes.FETCH_APPOINTMENTS_REQUEST, fetchAppointments)
}

export function* appointmentSaga() {
    yield all([
        watchfetchAppointments(),
    ])
}
