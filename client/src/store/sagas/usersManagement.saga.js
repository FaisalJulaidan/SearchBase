import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {solutionsActions, usersManagementActions} from "../actions";
import {http, alertError, alertSuccess, destroyMessage, loadingMessage, successMessage, errorMessage} from "../../helpers";

function* getUsers() {
    try {
        const res = yield http.get(`/users`);
        return yield put(usersManagementActions.getUsersSuccess(res.data.data))
    } catch (error) {
        console.log(error);
        return yield put(usersManagementActions.getUsersFailure(error.response.data));
    }
}

function* addUser(action) {
    try {
        loadingMessage('Adding new user...');
        const res = yield http.put(`/user`, action.params.user);

        yield successMessage('User Added');
        yield put(usersManagementActions.addUserSuccess(res.message));
        yield put(usersManagementActions.getUsers());
    } catch (error) {
        console.log(error.response);
        yield errorMessage('Error in adding User');
        yield put(usersManagementActions.addUserFailure(error.response.data));
    }
}

function* editUser(action) {
    try {
        loadingMessage('Editing user...');
        const res = yield http.post(`/user`, action.params.user);

        yield successMessage('User edited');
        yield put(usersManagementActions.editUserSuccess(res.message));
        yield put(usersManagementActions.getUsers())
    } catch (error) {
        console.log(error.response);
        yield errorMessage('Error in editing user');
        yield put(usersManagementActions.editUserFailure(error.response.data));
    }
}

function* deleteUser(action) {
    try {
        loadingMessage('Deleting user...');
        const res = yield http.post(`/user_delete`, action.params.user);

        yield successMessage('User deleted');
        yield put(usersManagementActions.deleteUserSuccess(res.message));
        yield put(usersManagementActions.getUsers())
    } catch (error) {
        console.log(error.response);
        yield errorMessage('Error in deleting User');
        yield put(usersManagementActions.deleteUserFailure(error.response.data));
    }
}


function* watchGetUsers() {
    yield takeEvery(actionTypes.GET_USERS_REQUEST, getUsers)
}

function* watchAddUser() {
    yield takeEvery(actionTypes.ADD_USER_REQUEST, addUser)
}

function* watchEditUser() {
    yield takeEvery(actionTypes.EDIT_USER_REQUEST, editUser)
}

function* watchDeleteUser() {
    yield takeEvery(actionTypes.DELETE_USER_REQUEST, deleteUser)
}


export function* usersManagementSaga() {
    yield all([
        watchGetUsers(),
        watchAddUser(),
        watchEditUser(),
        watchDeleteUser(),
    ])
}