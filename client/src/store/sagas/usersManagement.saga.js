import {all, put, takeEvery} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {usersManagementActions} from "../actions";
import {errorMessage, http, loadingMessage, successMessage} from "helpers";

function* getUsers() {
    try {
        const res = yield http.get(`/users`);
        return yield put(usersManagementActions.getUsersSuccess(res.data?.data?.users, res.data?.data?.roles))
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't load users";
        yield put(usersManagementActions.getUsersFailure(msg));
        errorMessage(msg);
    }
}

function* addUser(action) {
    try {
        loadingMessage('Adding new user...');
        const res = yield http.post(`/users`, action.params.user);
        yield put(usersManagementActions.addUserSuccess(res.message));
        yield put(usersManagementActions.getUsers());
        successMessage('New user added');

    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't add a new user";
        yield put(usersManagementActions.addUserFailure(msg));
        errorMessage(msg);
    }
}

function* editUser({userID, values}) {
    try {
        loadingMessage('Editing user...');
        const res = yield http.put(`/user/${userID}`, values);
        yield put(usersManagementActions.editUserSuccess(res.message));
        yield put(usersManagementActions.getUsers());
        successMessage('User edited');

    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't update the user";
        yield put(usersManagementActions.editUserFailure(msg));
        errorMessage(msg);
    }
}

function* deleteUser({userID}) {
    try {
        loadingMessage('Deleting user...');
        const res = yield http.delete(`/user/${userID}`);
        yield put(usersManagementActions.deleteUserSuccess(res.message));
        yield put(usersManagementActions.getUsers());
        successMessage('User deleted');

    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't delete the user";
        yield put(usersManagementActions.deleteUserFailure(msg));
        errorMessage(msg);
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
