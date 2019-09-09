import {all, put, takeEvery} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {appointmentActions} from "../actions";
import {errorMessage, http, loadingMessage, successMessage} from "helpers";

// import * as Sentry from '@sentry/browser';

function* fetchAppointments() {
    try {
        const res = yield http.get(`/appointments`);
        yield put(appointmentActions.fetchAppointmentsSuccess(res.data?.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't fetch appointments";
        yield put(appointmentActions.fetchAppointmentsFailure(msg));
        errorMessage(msg);
    }
}

function* setAppointmentStatus({appointmentID, status}) {
    try {
        const res = yield http.post('/appointments/set_status', {appointmentID, status});
        yield put(appointmentActions.setAppointmentStatusSuccess(appointmentID, status));
        successMessage(`Appointment ${status}`);
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't set appointment status";
        yield put(appointmentActions.setAppointmentStatusFailure(msg));
        errorMessage(msg);
    }
}

function* watchfetchAppointments() {
    yield takeEvery(actionTypes.FETCH_APPOINTMENTS_REQUEST, fetchAppointments)
}

function* watchSetAppointmentStatus() {
    yield takeEvery(actionTypes.SET_APPOINTMENT_STATUS_REQUEST, setAppointmentStatus)
}

export function* appointmentSaga() {
    yield all([
        watchfetchAppointments(),
        watchSetAppointmentStatus()
    ])
}
