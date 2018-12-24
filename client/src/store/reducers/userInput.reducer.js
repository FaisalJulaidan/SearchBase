import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {userInputs: [], isLoading: false, errorMsg: null};

export const userInput = (state = initialState, action) => {
    switch (action.type) {
        // Fetching user inputs
        case actionTypes.FETCH_USERINPUT_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.FETCH_USERINPUT_SUCCESS:
            console.log(action.userInputs);
            return updateObject(state, {
                userInputs: action.userInputs,
                isLoading: false
            });
        case actionTypes.FETCH_USERINPUT_FAILURE:
            return updateObject(state, {
                userInputs: [],
                isLoading: false,
                errorMsg: action.error.msg
            });

        //Clearing all user inputs
        case actionTypes.CLEAR_ALL_USERINPUT_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isClearingAll: true
            });
        case actionTypes.CLEAR_ALL_USERINPUT_SUCCESS:
            return updateObject(state, {
                isClearingAll: false,
                userInputs: [],
                errorMsg: null,
            });
        case actionTypes.CLEAR_ALL_USERINPUT_FAILURE:
            return updateObject(state, {
                isClearingAll: false,
                errorMsg: action.error.msg
            });
        default:
            return state
    }
};