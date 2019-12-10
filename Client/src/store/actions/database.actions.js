import * as actionTypes from './actionTypes';

const getDatabasesList = () => ({
    type: actionTypes.GET_DATABASES_LIST_REQUEST,
});

const getDatabasesListSuccess = (databasesList) => ({
    type: actionTypes.GET_DATABASES_LIST_SUCCESS,
    databasesList: databasesList
});

const getDatabasesListFailure = (error) => ({
    type: actionTypes.GET_DATABASES_LIST_FAILURE,
    error
});


// Upload
const uploadDatabase = (newDatabase) => ({
    type: actionTypes.UPLOAD_DATABASE_REQUEST,
    newDatabase
});


const uploadDatabaseSuccess = (successMessage, newDatabase) => ({
    type: actionTypes.UPLOAD_DATABASE_SUCCESS,
    successMessage,
    newDatabase
});

const uploadDatabaseFailure = (error) => ({
    type: actionTypes.UPLOAD_DATABASE_FAILURE,
    error
});


// Fetch
const fetchDatabase = (databaseID, pageNumber) => ({
    type: actionTypes.FETCH_DATABASE_REQUEST,
    meta: {thunk: true},
    databaseID,
    pageNumber
});

const fetchDatabaseSuccess = (successMessage, fetchedDatabase) => ({
    type: actionTypes.FETCH_DATABASE_SUCCESS,
    successMessage,
    fetchedDatabase,

});

const fetchDatabaseFailure = (error) => ({
    type: actionTypes.FETCH_DATABASE_FAILURE,
    error
});


// Fetch available candidates
const fetchAvailableCandidates = (databaseID) => ({
    type: actionTypes.FETCH_DATABASE_AVAILABLE_CANDIDATES_REQUEST,
    meta: {thunk: true},
    databaseID,
});

const fetchAvailableCandidatesSuccess = (successMessage, fetchedAvailableCandidates) => ({
    type: actionTypes.FETCH_DATABASE_AVAILABLE_CANDIDATES_SUCCESS,
    successMessage,
    fetchedAvailableCandidates,

});

const fetchAvailableCandidatesFailure = (error) => ({
    type: actionTypes.FETCH_DATABASE_AVAILABLE_CANDIDATES_FAILURE,
    error
});


// Reset (remove fetch database from reducer)
const resetFetchedDatabase = () => ({
    type: actionTypes.RESET_DATABASE
});

// Delete
const deleteDatabase = (databaseID) => ({
    type: actionTypes.DELETE_DATABASE_REQUEST,
    databaseID
});

const deleteDatabaseSuccess = (successMessage, databaseID) => ({
    type: actionTypes.DELETE_DATABASE_SUCCESS,
    successMessage,
    databaseID
});

const deleteDatabaseFailure = (error) => ({
    type: actionTypes.DELETE_DATABASE_FAILURE,
    error
});

// Update Database
const updateDatabase = (data, databaseID) => ({
    type: actionTypes.UPDATE_DATABASE_REQUEST,
    data,
    databaseID
});

const updateDatabaseSuccess = (successMessage, databaseID) => ({
    type: actionTypes.UPDATE_DATABASE_SUCCESS,
    successMessage,
    databaseID
});

const updateDatabaseFailure = (error) => ({
    type: actionTypes.UPDATE_DATABASE_FAILURE,
    error
});

export const databaseActions = {
    getDatabasesList,
    getDatabasesListSuccess,
    getDatabasesListFailure,

    uploadDatabase,
    uploadDatabaseSuccess,
    uploadDatabaseFailure,

    fetchDatabase,
    fetchDatabaseSuccess,
    fetchDatabaseFailure,
    resetFetchedDatabase,

    fetchAvailableCandidates,
    fetchAvailableCandidatesSuccess,
    fetchAvailableCandidatesFailure,

    updateDatabase,
    updateDatabaseSuccess,
    updateDatabaseFailure,

    deleteDatabase,
    deleteDatabaseSuccess,
    deleteDatabaseFailure,
};
