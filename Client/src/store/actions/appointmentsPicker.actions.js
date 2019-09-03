import * as actionTypes from './actionTypes';

const fetchAppointment = (token) => ({
    type: actionTypes.FETCH_APPOINTMENT_REQUEST,
    token
});

const fetchAppointmentSuccess = (appointment) => ({
    type: actionTypes.FETCH_APPOINTMENT_SUCCESS,
    appointment
});

const fetchAppointmentFailure = (error) => ({
    type: actionTypes.FETCH_APPOINTMENT_FAILURE,
    error
});


const selectAppointmentTime = (token, pickedTimeSlot, userTimeZone) => ({
    type: actionTypes.SELECT_APPOINTMENT_TIME_REQUEST,
    token,
    pickedTimeSlot,
    userTimeZone
});

const selectAppointmentTimeSuccess = (isSuccess) => ({
    type: actionTypes.SELECT_APPOINTMENT_TIME_SUCCESS,
    isSuccess
});

const selectAppointmentTimeFailure = (error) => ({
    type: actionTypes.SELECT_APPOINTMENT_TIME_FAILURE,
    error
});


export const appointmentsPickerActions = {
    fetchAppointment,
    fetchAppointmentSuccess,
    fetchAppointmentFailure,

    selectAppointmentTime,
    selectAppointmentTimeSuccess,
    selectAppointmentTimeFailure,
};
