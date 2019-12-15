import * as actionTypes from '../actions/actionTypes';
import {updateObject} from '../utility';

const initialState = {
    isLoading: false,
    isFetchedDatabaseLoading: false,
    isFetchedAvailableCandidatesLoading: false,
    errorMsg: null,
    databasesList: [],
    fetchedDatabase:{},
    fetchedAvailableCandidates:[]
};


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
                errorMsg: action
            });


        case actionTypes.FETCH_DATABASE_REQUEST:
            return updateObject(state, {
                isFetchedDatabaseLoading: true
            });
        case actionTypes.FETCH_DATABASE_SUCCESS:
            return updateObject(state, {
                isFetchedDatabaseLoading: false,
                fetchedDatabase: action.fetchedDatabase
            });
        case actionTypes.FETCH_DATABASE_FAILURE:
            return updateObject(state, {
                isFetchedDatabaseLoading: false,
                errorMsg: action.error
            });
        case actionTypes.RESET_DATABASE:
            return updateObject(state, {fetchedDatabase: {}});


        case actionTypes.FETCH_DATABASE_AVAILABLE_CANDIDATES_REQUEST:
            return updateObject(state, {
                isFetchedAvailableCandidatesLoading: true
            });
        case actionTypes.FETCH_DATABASE_AVAILABLE_CANDIDATES_SUCCESS:
            return updateObject(state, {
                isFetchedAvailableCandidatesLoading: false,
                fetchedAvailableCandidates: action.fetchedAvailableCandidates
            });
        case actionTypes.FETCH_DATABASE_AVAILABLE_CANDIDATES_FAILURE:
            return updateObject(state, {
                isFetchedAvailableCandidatesLoading: false,
                fetchedAvailableCandidates:[],
                errorMsg: action.error
            });


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
                errorMsg: action.error
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
                errorMsg: action.error
            });

        default:
            return state
    }
};