import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {appointment: {}};

export const appointmentsPicker = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.FETCH_APPOINTMENT_REQUEST:
            return updateObject(state, {
                errorMsg: null,
            });
        case actionTypes.FETCH_APPOINTMENT_SUCCESS:
            return updateObject(state, {
                appointment: action.appointment
            });
        case actionTypes.FETCH_APPOINTMENT_FAILURE:
            return updateObject(state, {
                errorMsg: action.error
            });

        default:
            return state
    }
};
