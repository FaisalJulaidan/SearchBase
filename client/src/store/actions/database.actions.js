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
const fetchDatabase = () => {
    return {
        type: actionTypes.FETCH_DATABASE_REQUEST,
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


// Delete
const DeleteDatabase = () => {
    return {
        type: actionTypes.DELETE_DATABASE_REQUEST,
    }
};

const DeleteDatabaseSuccess = (successMessage, databaseID) => {
    return {
        type: actionTypes.DELETE_DATABASE_SUCCESS,
        successMessage,
        databaseID
    }
};

const DeleteDatabaseFailure = (error) => {
    return {
        type: actionTypes.DELETE_DATABASE_FAILURE,
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

    DeleteDatabase,
    DeleteDatabaseSuccess,
    DeleteDatabaseFailure,
};