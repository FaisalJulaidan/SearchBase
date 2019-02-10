import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {solutionsActions, usersManagementActions} from "../actions";
import {http} from "../../helpers";
import {alertError, alertSuccess, destroyMessage, loadingMessage} from "../../helpers/alert";

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
        loadingMessage('Adding User');
        const res = yield http.put(`/user`, action.params.user);
        yield destroyMessage();
        yield alertSuccess('User Added', res.data.msg);
        yield put(usersManagementActions.addUserSuccess(res.message));
        yield put(usersManagementActions.getUsers());
    } catch (error) {
        console.log(error.response);
        yield destroyMessage();
        yield alertError('Error in adding User', error.response.data.msg);
        yield put(usersManagementActions.addUserFailure(error.response.data));
    }
}

function* editUser(action) {
    try {
        loadingMessage('Editing User');
        console.log("action.params", action.params)
        const res = yield http.post(`/user`, action.params.user);
        yield destroyMessage();
        yield alertSuccess('User Edited', res.data.msg);
        yield put(usersManagementActions.editUserSuccess(res.message));
        yield put(usersManagementActions.getUsers())
    } catch (error) {
        console.log(error.response);
        yield destroyMessage();
        yield alertError('Error in editing User', error.response.data.msg);
        yield put(usersManagementActions.editUserFailure(error.response.data));
    }
}

function* deleteUser(action) {
    try {
        loadingMessage('Deleting User');
        const res = yield http.post(`/user_delete`, action.params.user);
        yield destroyMessage();
        yield alertSuccess('User Deleted', res.data.msg);
        yield put(usersManagementActions.deleteUserSuccess(res.message));
        yield put(usersManagementActions.getUsers())
    } catch (error) {
        console.log(error.response);
        yield destroyMessage();
        yield alertError('Error in deleting User', error.response.data.msg);
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