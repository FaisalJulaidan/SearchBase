// AAT = AppointmentAllocationTime
import * as actionTypes from "./actionTypes";

const fetchAAT = (isSuccess, id) => ({
    type: actionTypes.FETCH_AAT_REQUEST,
    isSuccess,
    id
});

const fetchAATSuccess = (data) => ({
    type: actionTypes.FETCH_AAT_SUCCESS,
    allocationTimes: data
});

const fetchAATFailure = (error) => ({
    type: actionTypes.FETCH_AAT_FAILURE,
    error
});

const saveAAT = (newSettings) => ({
    type: actionTypes.SAVE_AAT_REQUEST,
    newSettings
});

const saveAATSuccess = () => ({
    type: actionTypes.SAVE_AAT_SUCCESS,
});

const saveAATFailure = (error) => ({
    type: actionTypes.SAVE_AAT_FAILURE,
    error
});




export const appointmentAllocationTimeActions = {
    fetchAAT,
    fetchAATSuccess,
    fetchAATFailure,
    saveAAT,
    saveAATSuccess,
    saveAATFailure
};
