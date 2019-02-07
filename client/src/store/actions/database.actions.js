import * as actionTypes from './actionTypes';

const getDatabasesList = () => {
    return {
        type: actionTypes.GET_DATABASES_LIST_REQUEST
    }
};

const getDatabasesListSuccess = (databasesList) => {
    return {
        type: actionTypes.GET_DATABASES_LIST_SUCCESS,
        databasesList
    }
};

const getDatabasesListFailure = (error) => {
    return {
        type: actionTypes.GET_DATABASES_LIST_FAILURE,
        error
    }
};


// Upload
const uploadDatabase = (database) => {
    return {
        type: actionTypes.UPLOAD_DATABASE_REQUEST,
        database
    }
};


const uploadDatabaseSuccess = (successMessage) => {
    return {
        type: actionTypes.UPLOAD_DATABASE_SUCCESS,
        successMessage
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

const fetchDatabaseSuccess = (successMessage, database) => {
    return {
        type: actionTypes.FETCH_DATABASE_SUCCESS,
        successMessage,
        database
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