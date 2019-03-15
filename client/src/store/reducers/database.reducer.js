import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {isLoading: false, errorMsg: null, databasesList: [], fetchedDatabase:{}};


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
                errorMsg: action.error
            });


        case actionTypes.FETCH_DATABASE_REQUEST:
            return updateObject(state, {
                isLoading: true
            });
        case actionTypes.FETCH_DATABASE_SUCCESS:
            return updateObject(state, {
                isLoading: false,
                fetchedDatabase: action.fetchedDatabase
            });
        case actionTypes.FETCH_DATABASE_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error.msg
            });
        case actionTypes.RESET_DATABASE:
            return updateObject(state, {fetchedDatabase: {}});


        case actionTypes.DELETE_DATABASE_REQUEST:
            return updateObject(state, {
                isDeletingDatabase: true
            });
        case actionTypes.DELETE_DATABASE_SUCCESS:
            let databasesList = [...state.databasesList].filter(db => db.ID !== action.databaseID);
            return updateObject(state, {
                isDeletingDatabase: false,
                databasesList: databasesList,
                fetchedDatabase: {}
            });
        case actionTypes.DELETE_DATABASE_FAILURE:
            return updateObject(state, {
                isDeletingDatabase: false,
                errorMsg: action.error.msg
            });


        case actionTypes.UPLOAD_DATABASE_REQUEST:
            return updateObject(state, {
                isLoading: true
            });
        case actionTypes.UPLOAD_DATABASE_SUCCESS:
            let updatedDatabaseList = [...state.databasesList];
            updatedDatabaseList.push(action.newDatabase);
            return updateObject(state, {
                isLoading: false,
                databasesList: updatedDatabaseList
            });
        case actionTypes.UPLOAD_DATABASE_FAILURE:
            return updateObject(state, {
                isLoading: false,
                errorMsg: action.error.msg
            });

        default:
            return state
    }
};