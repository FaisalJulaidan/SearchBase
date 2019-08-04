import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';
// import {deepClone} from "helpers";

const initialState = {appointments: [], isLoading: true, errorMsg: null};

export const appointment = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.FETCH_APPOINTMENTS_REQUEST:
            return updateObject(state, {
                appointments: [],
                isLoading: true,
            });
        case actionTypes.FETCH_APPOINTMENTS_SUCCESS:
            return updateObject(state, {
                appointments: action.appointments.map(a => ({...a, isLoading: false})),
                isLoading: false
            });
        case actionTypes.FETCH_APPOINTMENTS_FAILURE:
            return updateObject(state, {
                appointments: [],
                isLoading: false,
                errorMsg: action.error
            });
        case actionTypes.SET_APPOINTMENT_STATUS_REQUEST:
            console.log(action)
            return updateObject(state, {
                appointments: state.appointments.map(a => ({...a, isLoading: a.ID === action.appointmentID ? true : a.isLoading})),
            });
        case actionTypes.SET_APPOINTMENT_STATUS_SUCCESS:
            console.log(action  )
            return updateObject(state, {
                appointments: state.appointments.map(a => ({...a, ...(a.ID === action.id ? ({isLoading: false, Status: action.status}): ({}) )})),
                isLoading: false
            });
        case actionTypes.SET_APPOINTMENT_STATUS_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error
            });
        default:
            return state
    }
};
