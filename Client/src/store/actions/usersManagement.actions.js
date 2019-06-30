import * as actionTypes from './actionTypes';


const getUsers = () => ({
    type: actionTypes.GET_USERS_REQUEST
});

const getUsersSuccess = (usersList, roles) => ({
    type: actionTypes.GET_USERS_SUCCESS,
    usersList,
    roles
});

const getUsersFailure = (error) => ({
    type: actionTypes.GET_USERS_FAILURE,
    error
});

const addUser = (values) => ({
    type: actionTypes.ADD_USER_REQUEST,
    values
});

const addUserSuccess = (message) => ({
    type: actionTypes.ADD_USER_SUCCESS,
    message
});

const addUserFailure = (error) => ({
    type: actionTypes.ADD_USER_FAILURE,
    error
});

const editUser = (userID, values) => ({
    type: actionTypes.EDIT_USER_REQUEST,
    userID,
    values
});

const editUserSuccess = (message) => ({
    type: actionTypes.EDIT_USER_SUCCESS,
    message
});

const editUserFailure = (error) => ({
    type: actionTypes.EDIT_USER_FAILURE,
    error
});

const deleteUser = (userID) => ({
    type: actionTypes.DELETE_USER_REQUEST,
    userID
});

const deleteUserSuccess = (message) => ({
    type: actionTypes.DELETE_USER_SUCCESS,
    message
});

const deleteUserFailure = (error) => ({
    type: actionTypes.DELETE_USER_FAILURE,
    error
});

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
