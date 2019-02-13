import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {isLoading: false, errorMsg: null, databasesList: []};


export const database = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.GET_DATABASES_LIST_REQUEST:
            return updateObject(state, {
                isLoading: true
            });
        case actionTypes.GET_DATABASES_LIST_SUCCESS:
            return updateObject(state, {
                isLoading: false,
                databasesList: action.databasesList
            });
        case actionTypes.GET_DATABASES_LIST_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error.msg
            });

        case actionTypes.DELETE_DATABASE_REQUEST:
            return updateObject(state, {
                isDeletingGroup: true
            });
        case actionTypes.DELETE_DATABASE_SUCCESS:
            let databasesList = [...state.databasesList];
            const databaseToDeleteIndex =  databasesList.findIndex(db => db.ID === action.databaseID);
            databasesList.splice(databaseToDeleteIndex, 1);

            return updateObject(state, {
                isDeletingGroup: false,
                databasesList: action.databasesList
            });
        case actionTypes.DELETE_DATABASE_FAILURE:
            return updateObject(state, {
                isDeletingGroup: false,
                errorMsg: action.error.msg
            });


        default:
            return state
    }
};