import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {
    availability: [],
    isLoading: false,
    errorMsg: null
};

export const availability = (state = initialState, action) => {
    switch (action.type) {

        //Fetch campaign data
        case actionTypes.FETCH_AVAILABILITY_REQUEST:
            return updateObject(state, {
              availability: [],
              isLoading: true,
            });
        case actionTypes.FETCH_AVAILABILITY_SUCCESS:
            return updateObject(state, {
              availability: action.availability,
              isLoading: false,
              errorMsg: null
            });
        case actionTypes.FETCH_AVAILABILITY_FAILURE:
            return updateObject(state, {
              availabilityList: [],
              isLoading: false,
              errorMsg: action.errorMsg
            });
        default:
            return state;
    }
};