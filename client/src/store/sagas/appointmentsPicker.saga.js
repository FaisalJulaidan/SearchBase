import {all, put, takeEvery} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {appointmentsPickerActions} from "../actions";
import {errorMessage, http, successMessage} from "helpers";


function* fetchAppointment({token}) {
    try {
        const res = yield http.get(`appointments/${token}`);
        yield put(appointmentsPickerActions.fetchAppointmentSuccess(res.data.data));
    } catch (error) {
        const msg = error.response?.data?.msg || 'Couldn\'t fetch appointment data';
        errorMessage(msg);
        yield put(appointmentsPickerActions.fetchAppointmentFailure(msg));
    }
}

function* selectAppointmentTime({token, pickedTimeSlot}) {
    try {
        const res = yield http.post(`appointments/${token}`, {pickedTimeSlot});
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
