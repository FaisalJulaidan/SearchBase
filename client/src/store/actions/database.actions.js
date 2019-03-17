import * as actionTypes from './actionTypes';

const getDatabasesList = () => {
    return {
        type: actionTypes.GET_DATABASES_LIST_REQUEST,
    }
};

const getDatabasesListSuccess = (databasesList) => {
    return {
        type: actionTypes.GET_DATABASES_LIST_SUCCESS,
        databasesList: databasesList
    }
};

const getDatabasesListFailure = (error) => {
    return {
        type: actionTypes.GET_DATABASES_LIST_FAILURE,
        error
    }
};


// Upload
const uploadDatabase = (newDatabase) => {
    return {
        type: actionTypes.UPLOAD_DATABASE_REQUEST,
        newDatabase
    }
};


const uploadDatabaseSuccess = (successMessage, newDatabase) => {
    return {
        type: actionTypes.UPLOAD_DATABASE_SUCCESS,
        successMessage,
        newDatabase
    }
};

const uploadDatabaseFailure = (error) => {
    return {
        type: actionTypes.UPLOAD_DATABASE_FAILURE,
        error
    }
};


// Fetch
const fetchDatabase = (databaseID, pageNumber) => {
    return {
        type: actionTypes.FETCH_DATABASE_REQUEST,
        databaseID,
        pageNumber
    }
};

const fetchDatabaseSuccess = (successMessage, fetchedDatabase) => {
    return {
        type: actionTypes.FETCH_DATABASE_SUCCESS,
        successMessage,
        fetchedDatabase
    }
};

const fetchDatabaseFailure = (error) => {
    return {
        type: actionTypes.FETCH_DATABASE_FAILURE,
        error
    }
};
const resetFetchedDatabase = () => {
    return {
        type: actionTypes.RESET_DATABASE
    }
};

// Delete
const deleteDatabase = (databaseID) => {
    return {
        type: actionTypes.DELETE_DATABASE_REQUEST,
        databaseID
    }
};

const deleteDatabaseSuccess = (successMessage, databaseID) => {
    return {
        type: actionTypes.DELETE_DATABASE_SUCCESS,
        successMessage,
        databaseID
    }
};

const deleteDatabaseFailure = (error) => {
    return {
        type: actionTypes.DELETE_DATABASE_FAILURE,
        error
    }
};

// Update Database
const updateDatabase = (data, databaseID) => {
    return {
        type: actionTypes.UPDATE_DATABASE_REQUEST,
        data,
        databaseID
    }
};

const updateDatabaseSuccess = (successMessage, databaseID) => {
    return {
        type: actionTypes.UPDATE_DATABASE_SUCCESS,
        successMessage,
        databaseID
    }
};

const updateDatabaseFailure = (error) => {
    return {
        type: actionTypes.UPDATE_DATABASE_FAILURE,
        error
    }
};

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

    updateDatabase,
    updateDatabaseSuccess,
    updateDatabaseFailure,

    deleteDatabase,
    deleteDatabaseSuccess,
    deleteDatabaseFailure,
};