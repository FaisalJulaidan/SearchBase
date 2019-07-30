// AAT = AppointmentAllocationTime
import * as actionTypes from "./actionTypes";

const fetchAAT = (isSuccess, id) => ({
    type: actionTypes.FETCH_AAT_REQUEST,
    isSuccess,
    id
});

const fetchAATSuccess = (error) => ({
    type: actionTypes.FETCH_AAT_SUCCESS,
    error
});

const fetchAATFailure = (error) => ({
    type: actionTypes.FETCH_AAT_FAILURE,
    error
});



export const appointmentAllocationTimeActions = {
    fetchAAT,
    fetchAATSuccess,
    fetchAATFailure,
};
