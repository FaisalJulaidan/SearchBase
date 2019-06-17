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


const selectAppointmentTime = (token, pickedTimeSlot) => {
    return {
        type: actionTypes.SELECT_APPOINTMENT_TIME_REQUEST,
        token,
        pickedTimeSlot
    };
};

const selectAppointmentTimeSuccess = (isSuccess) => {
    return {
        type: actionTypes.SELECT_APPOINTMENT_TIME_SUCCESS,
        isSuccess
    };
};

const selectAppointmentTimeFailure = (error) => {
    return {
        type: actionTypes.SELECT_APPOINTMENT_TIME_FAILURE,
        error
    };
};


export const appointmentsPickerActions = {
    fetchAppointment,
    fetchAppointmentSuccess,
    fetchAppointmentFailure,

    selectAppointmentTime,
    selectAppointmentTimeSuccess,
    selectAppointmentTimeFailure,


};
