import {all, put, takeEvery} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {appointmentAllocationTimeActions} from "../actions";
import {errorMessage, http, successMessage} from "helpers";
import axios from 'axios';


function* fetchAppointmentAllocationTime({id}) {
    try {
        const res = yield axios.get(`/api/allocation_times/${id}`,
            {headers: {'Content-Type': 'application/json'}});

        yield put(appointmentAllocationTimeActions.fetchAATSuccess(res.data.data));
    } catch (error) {
        const msg = error.response?.data?.msg || 'Couldn\'t fetch appointment data';
        errorMessage(msg);
        yield put(appointmentAllocationTimeActions.fetchAppointmentFailure(msg));
    }
}

function* watchFetchAppointmentAllocationTime() {
    yield takeEvery(actionTypes.FETCH_AAT_REQUEST, fetchAppointmentAllocationTime)
}


export function* appointmentAllocationTimeSaga() {
    yield all([
        watchFetchAppointmentAllocationTime(),
    ])
}
