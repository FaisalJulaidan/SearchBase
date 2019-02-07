import * as actionTypes from './actionTypes';


const getUsers = () => {
    return {
        type: actionTypes.GET_USERS_REQUEST
    };
};

const getUsersSuccess = (usersData) => {
    return {
        type: actionTypes.GET_USERS_SUCCESS,
        usersData
    };
};

const getUsersFailure = (error) => {
    return {
        type: actionTypes.GET_USERS_FAILURE,
        error
    };
};

export const usersManagementActions = {
    getUsers,
    getUsersSuccess,
    getUsersFailure,
};