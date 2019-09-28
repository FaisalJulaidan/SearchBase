import * as actionTypes from './actionTypes';

const fetchAvailability = (assistantID) => {
  return {
  type: actionTypes.FETCH_AVAILABILITY_REQUEST,
  assistantID
  }
}
const fetchAvailabilitySuccess = (availability) => {
    return {
        type: actionTypes.FETCH_APPOINTMENTS_SUCCESS,
        availability
    };
};

const fetchAvailabilityFailure = (errorMsg) => {
    return {
        type: actionTypes.FETCH_APPOINTMENTS_FAILURE,
        errorMsg
    };
}

export const availabilityActions = {
  fetchAvailability,
  fetchAvailabilitySuccess,
  fetchAvailabilityFailure
}