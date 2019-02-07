import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {usersManagementActions} from "../actions";
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


function* watchGetUsers() {
    yield takeEvery(actionTypes.GET_USERS_REQUEST, getUsers)
}


export function* usersManagementSaga() {
    yield all([
        watchGetUsers()
    ])
}