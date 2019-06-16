import * as actionTypes from './actionTypes';

const fetchAppointment = (token) => {
    return {
        type: actionTypes.FETCH_APPOINTMENT_REQUEST,
        token
    };
};

const fetchAppointmentSuccess = (appointment) => {
    return {
        type: actionTypes.FETCH_APPOINTMENT_SUCCESS,
        appointment
    };
};

const fetchAppointmentFailure = (error) => {
    return {
        type: actionTypes.FETCH_APPOINTMENT_FAILURE,
        error
    };
};


export const appointmentsPickerActions = {
    fetchAppointment,
    fetchAppointmentSuccess,
    fetchAppointmentFailure,

};
