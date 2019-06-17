import * as actionTypes from './actionTypes';


const getUsers = () => {
    return {
        type: actionTypes.GET_USERS_REQUEST
    };
};

const getUsersSuccess = (usersList, roles) => {
    return {
        type: actionTypes.GET_USERS_SUCCESS,
        usersList,
        roles
    };
};

const getUsersFailure = (error) => {
    return {
        type: actionTypes.GET_USERS_FAILURE,
        error
    };
};

const addUser = (params) => {
    return {
        type: actionTypes.ADD_USER_REQUEST,
        params
    };
};

const addUserSuccess = (message) => {
    return {
        type: actionTypes.ADD_USER_SUCCESS,
        message
    };
};

const addUserFailure = (error) => {
    return {
        type: actionTypes.ADD_USER_FAILURE,
        error
    };
};

const editUser = (userID, values) => {
    return {
        type: actionTypes.EDIT_USER_REQUEST,
        userID,
        values
    };
};

const editUserSuccess = (message) => {
    return {
        type: actionTypes.EDIT_USER_SUCCESS,
        message
    };
};

const editUserFailure = (error) => {
    return {
        type: actionTypes.EDIT_USER_FAILURE,
        error
    };
};

const deleteUser = (userID) => {
    return {
        type: actionTypes.DELETE_USER_REQUEST,
        userID
    };
};

const deleteUserSuccess = (message) => {
    return {
        type: actionTypes.DELETE_USER_SUCCESS,
        message
    };
};

const deleteUserFailure = (error) => {
    return {
        type: actionTypes.DELETE_USER_FAILURE,
        error
    };
};

export const usersManagementActions = {
    getUsers,
    getUsersSuccess,
    getUsersFailure,
    addUser,
    addUserSuccess,
    addUserFailure,
    editUser,
    editUserSuccess,
    editUserFailure,
    deleteUser,
    deleteUserSuccess,
    deleteUserFailure
};