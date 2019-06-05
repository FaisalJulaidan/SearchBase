import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';
// import {deepClone} from "helpers";

const initialState = {analytics: [], isLoading: true, errorMsg: null};

export const analytics = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.FETCH_ANALYTICS_REQUEST:
            return updateObject(state, {
                analytics: [],
                isLoading: true,
            });
        case actionTypes.FETCH_ANALYTICS_SUCCESS:
            return updateObject(state, {
                analytics: action.analytics,
                isLoading: false
            });
        case actionTypes.FETCH_ANALYTICS_FAILURE:
            return updateObject(state, {
                assistantList: [],
                isLoading: false,
                errorMsg: action.error
            });
        default:
            return state
    }
};
