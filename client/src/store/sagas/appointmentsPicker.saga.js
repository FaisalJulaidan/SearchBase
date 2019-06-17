import {all, put, takeEvery} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {appointmentsPickerActions} from "../actions";
import {errorMessage, http, successMessage} from "helpers";
import axios from 'axios';


function* fetchAppointment({token}) {
    try {
        const res = yield axios.get(`/api/appointments/${token}`,
            {headers: {'Content-Type': 'application/json'}});

        yield put(appointmentsPickerActions.fetchAppointmentSuccess(res.data.data));
    } catch (error) {
        const msg = error.response?.data?.msg || 'Couldn\'t fetch appointment data';
        errorMessage(msg);
        yield put(appointmentsPickerActions.fetchAppointmentFailure(msg));
    }
}

function* selectAppointmentTime({token, pickedTimeSlot}) {
    try {
        const res = yield axios.post(`/api/appointments/${token}`, {pickedTimeSlot},
            {headers: {'Content-Type': 'application/json'}});
        successMessage(res.data?.msg || 'Appointment selected successfully');
        yield put(appointmentsPickerActions.selectAppointmentTimeSuccess());
    } catch (error) {
        const msg = error.response?.data?.msg || 'Appointment selection failed';
        errorMessage(msg);
        yield put(appointmentsPickerActions.selectAppointmentTimeFailure(msg));
    }
}

function* watchSelectAppointmentTime() {
    yield takeEvery(actionTypes.SELECT_APPOINTMENT_TIME_REQUEST, selectAppointmentTime)
}


function* watchFetchAppointment() {
    yield takeEvery(actionTypes.FETCH_APPOINTMENT_REQUEST, fetchAppointment)
}


export function* appointmentsPickerSaga() {
    yield all([
        watchFetchAppointment(),
        watchSelectAppointmentTime()
    ])
}
