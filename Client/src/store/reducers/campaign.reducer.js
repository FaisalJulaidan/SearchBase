import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {campaign: null, isLaunching: true, errorMsg: null};

export const campaign = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.LAUNCH_CAMPAIGN_REQUEST:
            return updateObject(state, {
                isLaunching: true,
                errorMsg: null,
            });
        case actionTypes.LAUNCH_CAMPAIGN_SUCCESS:
            return updateObject(state, {
                isLaunching: false,
            });
        case actionTypes.LAUNCH_CAMPAIGN_FAILURE:
            return updateObject(state, {
                isLaunching: false,
                errorMsg: action.error
            });
        default:
            return state;
    }
};