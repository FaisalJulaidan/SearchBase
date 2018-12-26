import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {solutionsData: {}, isLoading: false, errorMsg: null};

export const solutions = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.GET_SOLUTIONS_REQUEST:
            return updateObject(state, {
                solutionsData: {},
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
                solutionsData: {},
                isLoading: false,
                errorMsg: action.error.msg
            });
        default:
            return state
    }
};