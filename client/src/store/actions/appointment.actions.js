import * as actionTypes from './actionTypes';


const fetchAppointments = () => {
    return {
        type: actionTypes.FETCH_APPOINTMENTS_REQUEST
    };
};

const fetchAppointmentsSuccess = (appointments) => {
    return {
        type: actionTypes.FETCH_APPOINTMENTS_SUCCESS,
        appointments
    };
};

const fetchAppointmentsFailure = (error) => {
    return {
        type: actionTypes.FETCH_APPOINTMENTS_FAILURE,
        error
    };
};

const setAppointmentStatusRequest = () => {
    return {
        type: actionTypes.SET_APPOINTMENT_STATUS_REQUEST,
    };
};

const setAppointmentStatusSuccess = (status) => {
    return {
        type: actionTypes.SET_APPOINTMENT_STATUS_SUCCESS,
        status
    };
};

const setAppointmentStatusFailure = (error) => {
    return {
        type: actionTypes.SET_APPOINTMENT_STATUS_FAILURE,
        error
    };
};

export const appointmentActions = {
    fetchAppointments,
    fetchAppointmentsSuccess,
    fetchAppointmentsFailure,

    setAppointmentStatusRequest,
    setAppointmentStatusSuccess,
    setAppointmentStatusFailure
};
