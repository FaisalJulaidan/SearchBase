import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {appointment: {}, isSuccess: false, isSelected: false};

export const appointmentsPicker = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.FETCH_APPOINTMENT_REQUEST:
            return updateObject(state, {
                errorMsg: null,
            });
        case actionTypes.FETCH_APPOINTMENT_SUCCESS:
            return updateObject(state, {
                appointment: action.appointment,
                isSuccess: false,
                isSelected: false
            });
        case actionTypes.FETCH_APPOINTMENT_FAILURE:
            return updateObject(state, {
                errorMsg: action.error
            });

        case actionTypes.SELECT_APPOINTMENT_TIME_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isSelected: false
            });
        case actionTypes.SELECT_APPOINTMENT_TIME_SUCCESS:
            return updateObject(state, {
                isSuccess: true,
                isSelected: true
            });
        case actionTypes.SELECT_APPOINTMENT_TIME_FAILURE:
            return updateObject(state, {
                errorMsg: action.error,
                isSuccess: false,
                isSelected: true
            });


        default:
            return state
    }
};
