import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {usersList: [], isLoading: false, errorMsg: null};

export const usersManagement = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.GET_USERS_REQUEST:
            return updateObject(state, {
                usersList: [],
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.GET_USERS_SUCCESS:
            return updateObject(state, {
                usersList: action.usersData,
                isLoading: false
            });
        case actionTypes.GET_USERS_FAILURE:
            return updateObject(state, {
                usersList: [],
                isLoading: false,
                errorMsg: action.error.msg
            });

        default:
            return state
    }
};