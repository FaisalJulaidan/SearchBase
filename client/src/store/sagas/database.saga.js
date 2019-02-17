import * as actionTypes from '../actions/actionTypes';
import {put, takeEvery, takeLatest, all} from 'redux-saga/effects'
import {databaseActions, flowActions} from "../actions";
import {alertSuccess, http} from "../../helpers";
import {alertError, destroyMessage, loadingMessage} from "../../helpers/alert";


function* getDatabasesList() {
    try {
        loadingMessage('Loading databases list');
        const res = yield http.get(`/databases`);
        yield put(databaseActions.getDatabasesListSuccess(res.data.data));
        yield destroyMessage();
    } catch (error) {
        console.log(error);
        yield destroyMessage();
        yield alertError('Loading databases list Unsuccessful', error.response.data.msg);
        yield put(databaseActions.getDatabasesListFailure(error.response.data));
    }
}

function* watchGetDatabaseList() {
    yield takeLatest(actionTypes.GET_DATABASES_LIST_REQUEST, getDatabasesList)
}

function* fetchDatabases({databaseID}) {
    try {
        loadingMessage('Loading database', 0);
        const res = yield http.get(`/databases/${databaseID}`);
        yield put(databaseActions.fetchDatabaseSuccess(res.data.msg, res.data.data));
        yield destroyMessage();
    } catch (error) {
        console.log(error);
        yield destroyMessage();
        yield alertError('Loading database Unsuccessful', error.response.data.msg);
        yield put(databaseActions.fetchDatabaseFailure(error.response.data));
    }
}

function* watchFetchDatabases() {
    yield takeLatest(actionTypes.FETCH_DATABASE_REQUEST, fetchDatabases)
}

function* uploadDatabase({newDatabase}) {
    try {
        loadingMessage('Adding database', 0);
        const res = yield http.post(`/databases`, newDatabase);
        yield destroyMessage();
        yield alertSuccess('Database added', res.data.msg);
        yield put(databaseActions.uploadDatabaseSuccess(res.data.msg, res.data.data));

    } catch (error) {
        console.log(error);
        yield destroyMessage();
        yield alertError('Adding database faild', error.response.data.msg);
        yield put(databaseActions.uploadDatabaseFailure(error.response.data));
    }
}

function* watchAddDatabase() {
    yield takeLatest(actionTypes.UPLOAD_DATABASE_REQUEST, uploadDatabase)
}

export function* databaseSaga() {
    yield all([
        watchGetDatabaseList(),
        watchFetchDatabases(),
        watchAddDatabase()
    ])
}
