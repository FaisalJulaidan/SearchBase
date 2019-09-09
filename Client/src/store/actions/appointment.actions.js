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

const setAppointmentStatusRequest = (appointmentID, status, name, email, phone) => {
    return {
        type: actionTypes.SET_APPOINTMENT_STATUS_REQUEST,
        appointmentID,
        name,
        email,
        phone,
        status
    };
};

const setAppointmentStatusSuccess = (id, status) => {
    return {
        type: actionTypes.SET_APPOINTMENT_STATUS_SUCCESS,
        id,
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
