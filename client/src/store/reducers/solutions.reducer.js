import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {solutionsData: {}, isLoading: false, errorMsg: null};

export const solutions = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.GET_SOLUTIONS_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.GET_SOLUTIONS_SUCCESS:
            return updateObject(state, {
                solutionsData: action.solutionsData,
                isLoading: false
            });
        case actionTypes.GET_SOLUTIONS_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error.msg
            });
        case actionTypes.ADD_SOLUTION_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.ADD_SOLUTION_SUCCESS:
            return updateObject(state, {
                isLoading: false,
                message: action.message
            });
        case actionTypes.ADD_SOLUTION_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error.msg
            });
        case actionTypes.EDIT_SOLUTION_REQUEST:
            return updateObject(state, {
                errorMsg: null,
                isLoading: true
            });
        case actionTypes.EDIT_SOLUTION_SUCCESS:
            return updateObject(state, {
                isLoading: false,
                message: action.message
            });
        case actionTypes.EDIT_SOLUTION_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error.msg
            });
        default:
            return state
    }
};