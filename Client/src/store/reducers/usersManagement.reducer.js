import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {usersList: [], roles:[], isLoading: false, errorMsg: null};

export const usersManagement = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.GET_USERS_REQUEST:
            return updateObject(state, {
                usersList: [],
                roles:[],
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.GET_USERS_SUCCESS:
            return updateObject(state, {
                usersList: action.usersList,
                roles: action.roles,
                isLoading: false
            });
        case actionTypes.GET_USERS_FAILURE:
            return updateObject(state, {
                usersList: [],
                roles: [],
                isLoading: false,
                errorMsg: action.error
            });
        case actionTypes.ADD_USER_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.ADD_USER_SUCCESS:
            return updateObject(state, {
                isLoading: false
            });
        case actionTypes.ADD_USER_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error
            });
        case actionTypes.EDIT_USER_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.EDIT_USER_SUCCESS:
            return updateObject(state, {
                isLoading: false
            });
        case actionTypes.EDIT_USER_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error
            });
        case actionTypes.DELETE_USER_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.DELETE_USER_SUCCESS:
            return updateObject(state, {
                isLoading: false
            });
        case actionTypes.DELETE_USER_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error
            });

        default:
            return state
    }
};