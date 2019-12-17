import { all, put, takeEvery } from 'redux-saga/effects';
import * as actionTypes from '../actions/actionTypes';
import { appointmentsPickerActions } from '../actions';
import { errorMessage, successMessage } from 'helpers';
import axios from 'axios';


function* fetchAppointment({token}) {
    try {
        const res = yield axios.get(`${process.env.REACT_APP_ENV!=='development'? process.env.REACT_APP_API_URL:''}/api/allocation_times/${token}`,
            {headers: {'Content-Type': 'application/json'}});

        yield put(appointmentsPickerActions.fetchAppointmentSuccess(res.data.data));
    } catch (error) {
        const msg = error.response?.data?.msg || 'Couldn\'t fetch appointment data';
        errorMessage(msg);
        yield put(appointmentsPickerActions.fetchAppointmentFailure(msg));
    }
}

function* selectAppointmentTime({ token, pickedTimeSlot, userTimeZone }) {
    try {
        const res = yield axios.post(`${process.env.REACT_APP_ENV!=='development'? process.env.REACT_APP_API_URL:''}/api/allocation_times/${token}`,
            { pickedTimeSlot, userTimeZone },
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
