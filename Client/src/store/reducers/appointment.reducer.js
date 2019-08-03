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
                appointments: action.appointments,
                isLoading: false
            });
        case actionTypes.FETCH_APPOINTMENTS_FAILURE:
            return updateObject(state, {
                appointments: [],
                isLoading: false,
                errorMsg: action.error
            });
        case actionTypes.SET_APPOINTMENT_STATUS_REQUEST:
            return updateObject(state, {
                isLoading: true,
            });
        case actionTypes.SET_APPOINTMENT_STATUS_SUCCESS:
            console.log(action  )
            return updateObject(state, {
                appointments: state.appointments.map(a => ({...a, Status: a.ID === action.id ? action.status : a.Status})),
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
