// AAT = AppointmentAllocationTime
import * as actionTypes from "./actionTypes";

const fetchAAT = (isSuccess, id) => ({
    type: actionTypes.FETCH_AAT_REQUEST,
    isSuccess,
    id
});

const fetchAATSuccess = (data, aat) => ({
    type: actionTypes.FETCH_AAT_SUCCESS,
    allocationTimes: data,
    aat: aat
});

const fetchAATFailure = (error) => ({
    type: actionTypes.FETCH_AAT_FAILURE,
    error
});

const saveAAT = (newSettings) => ({
    type: actionTypes.SAVE_AAT_REQUEST,
    newSettings
});

const saveAATSuccess = (customID, id) => ({
    type: actionTypes.SAVE_AAT_SUCCESS,
    customID,
    id
});

const saveAATFailure = (error) => ({
    type: actionTypes.SAVE_AAT_FAILURE,
    error
});

const createAAT = (aat) => ({
    type: actionTypes.CREATE_AAT_REQUEST,
    aat
})

const createAATSuccess = (aat) => ({
    type: actionTypes.CREATE_AAT_SUCCESS,
    aat
});

const createAATFailure = (error) => ({
    type: actionTypes.CREATE_AAT_FAILURE,
    error
});

const switchActiveAAT = (id) => ({
    type: actionTypes.SWITCH_ACTIVE_AAT,
    id
})


export const appointmentAllocationTimeActions = {
    fetchAAT,
    fetchAATSuccess,
    fetchAATFailure,
    saveAAT,
    saveAATSuccess,
    saveAATFailure,
    createAAT,
    createAATSuccess,
    createAATFailure,
    switchActiveAAT
};
