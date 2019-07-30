import {all, put, takeEvery} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {appointmentAllocationTimeActions} from "../actions";
import {errorMessage, http, successMessage} from "helpers";
import axios from 'axios';


function* fetchAppointmentAllocationTime() {
    try {
        const res = yield http.get(`/allocation_times_list/`,
            {headers: {'Content-Type': 'application/json'}});
        console.log(res.data.data)
        yield put(appointmentAllocationTimeActions.fetchAATSuccess(res.data.data));
    } catch (error) {
        const msg = error.response?.data?.msg || 'Couldn\'t fetch appointment data';
        errorMessage(msg);
        yield put(appointmentAllocationTimeActions.fetchAATFailure(msg));
    }
}

function* watchFetchAppointmentAllocationTime() {
    // console.log('taking')
    yield takeEvery(actionTypes.FETCH_AAT_REQUEST, fetchAppointmentAllocationTime)
}


export function* appointmentAllocationTimeSaga() {
    yield all([
        watchFetchAppointmentAllocationTime(),
    ])
}
