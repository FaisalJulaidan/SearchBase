import {all, put, takeEvery} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {appointmentAllocationTimeActions} from "../actions";
import {errorMessage, http, successMessage} from "helpers";


function* fetchAppointmentAllocationTime() {
    try {
        const res = yield http.get(`/allocation_times_list/`,
            {headers: {'Content-Type': 'application/json'}});
        yield put(appointmentAllocationTimeActions.fetchAATSuccess(res.data.data, res.data.data[0]));
    } catch (error) {
        const msg = error.response?.data?.msg || 'Couldn\'t fetch appointment data';
        errorMessage(msg);
        yield put(appointmentAllocationTimeActions.fetchAATFailure(msg));
    }
}

function* saveAppointmentAllocationTime({newSettings}) {
    try {
        const res = yield http.post(`/allocation_times/save`, newSettings,
            {headers: {'Content-Type': 'application/json'}});
        yield put(appointmentAllocationTimeActions.saveAATSuccess(res.data.data));
        successMessage("Successfully saved Appointment Allocation Timetable")
    } catch (error) {
        const msg = error.response?.data?.msg || 'Couldn\'t save Appointment Allocation Timetable';
        errorMessage(msg);
        yield put(appointmentAllocationTimeActions.saveAATFailure(msg));
    }
}

function* createAppointmentAllocationTime({aat}) {
    try {
        console.log(aat)
        const res = yield http.post(`/allocation_times/create`, aat,
            {headers: {'Content-Type': 'application/json'}});
        yield put(appointmentAllocationTimeActions.createAATSuccess(res.data.data[0]));
        successMessage("Successfully created Appointment Allocation Timetable")
    } catch (error) {
        const msg = error.response?.data?.msg || 'Couldn\'t create Appointment Allocation Timetable';
        errorMessage(msg);
        console.log(error)
        yield put(appointmentAllocationTimeActions.deleteAATFailure(msg));
    }
}

function* deleteAppointmentAllocationTime({id}) {
    try {
        yield http.get(`/allocation_times/${id}/delete`,
            {headers: {'Content-Type': 'application/json'}});
        yield put(appointmentAllocationTimeActions.deleteAATSuccess(id));
        successMessage("Successfully delete Appointment Allocation Timetable")
    } catch (error) {
        const msg = error.response?.data?.msg || 'Couldn\'t delete Appointment Allocation Timetable';
        errorMessage(msg);
        console.log(error)
        yield put(appointmentAllocationTimeActions.deleteAATFailure(msg));
    }
}

function* watchCreateAppointmentAllocationTime() {
    yield takeEvery(actionTypes.CREATE_AAT_REQUEST, createAppointmentAllocationTime)
}

function* watchFetchAppointmentAllocationTime() {
    yield takeEvery(actionTypes.FETCH_AAT_REQUEST, fetchAppointmentAllocationTime)
}

function* watchSaveAppointmentAllocationTime() {
    yield takeEvery(actionTypes.SAVE_AAT_REQUEST, saveAppointmentAllocationTime)
}

function* watchDeleteAppointmentAllocationTime() {
    yield takeEvery(actionTypes.DELETE_AAT_REQUEST, deleteAppointmentAllocationTime)
}

export function* appointmentAllocationTimeSaga() {
    yield all([
        watchFetchAppointmentAllocationTime(),
        watchSaveAppointmentAllocationTime(),
        watchCreateAppointmentAllocationTime(),
        watchDeleteAppointmentAllocationTime()
    ])
}
