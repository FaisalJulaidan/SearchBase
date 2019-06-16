import {all, put, takeEvery} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {appointmentsPickerActions} from "../actions";
import {errorMessage, http} from "helpers";


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

function* watchFetchAppointment() {
    yield takeEvery(actionTypes.FETCH_APPOINTMENT_REQUEST, fetchAppointment)
}


export function* appointmentsPickerSaga() {
    yield all([
        watchFetchAppointment()
    ])
}
