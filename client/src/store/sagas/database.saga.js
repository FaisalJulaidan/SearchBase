import * as actionTypes from '../actions/actionTypes';
import {put, takeEvery, takeLatest, all} from 'redux-saga/effects'
import {databaseActions, flowActions} from "../actions";
import {http, successMessage, loadingMessage, errorMessage} from "../../helpers";


function* getDatabasesList() {
    try {
        loadingMessage('Loading databases list');
        const res = yield http.get(`/databases`);
        yield put(databaseActions.getDatabasesListSuccess(res.data.data));
        successMessage('Databases loaded')
    } catch (error) {
        console.log(error);
        yield put(databaseActions.getDatabasesListFailure(error.response.data));
        errorMessage("Couldn't load databases list");

    }
}
function* watchGetDatabaseList() {
    yield takeLatest(actionTypes.GET_DATABASES_LIST_REQUEST, getDatabasesList)
}

// ==================================================================

function* fetchDatabase({databaseID}) {
    try {
        loadingMessage('Loading database...', 0);
        const res = yield http.get(`/databases/${databaseID}`);
        yield put(databaseActions.fetchDatabaseSuccess(res.data.msg, res.data.data));
        successMessage('Database loaded');
    } catch (error) {
        console.log(error);
        errorMessage("Couldn't load database");
        yield put(databaseActions.fetchDatabaseFailure(error.response.data));
    }
}
function* watchFetchDatabase() {
    yield takeLatest(actionTypes.FETCH_DATABASE_REQUEST, fetchDatabase)
}


// ==================================================================

function* uploadDatabase({newDatabase}) {
    try {
        loadingMessage('Uploading database...', 0);
        const res = yield http.post(`/databases`, newDatabase);
        successMessage('Database uploaded');
        yield put(databaseActions.uploadDatabaseSuccess(res.data.msg, res.data.data));

    } catch (error) {
        console.log(error);
        yield put(databaseActions.uploadDatabaseFailure(error.response.data));
        errorMessage("Couldn't upload database");
    }
}
function* watchAddDatabase() {
    yield takeLatest(actionTypes.UPLOAD_DATABASE_REQUEST, uploadDatabase)
}

// ==================================================================

function* deleteDatabase({deletedDatabase}) {
    try {
        console.log(deletedDatabase)
        loadingMessage('Deleteing database...', 0);
        const res = yield http.delete(`/databases`, {deletedDatabase: deletedDatabase.databaseInfo});
        successMessage('Database Deleted');
        yield put(databaseActions.deleteDatabaseSuccess(res.data.msg, res.data.data));

    } catch (error) {
        console.log(error);
        yield put(databaseActions.deleteDatabaseFailure(error.response.data));
        errorMessage("Couldn't delete database");
    }
}

function* watchDeleteDatabase() {
    yield takeLatest(actionTypes.DELETE_DATABASE_REQUEST, deleteDatabase)
}

// ==================================================================

function* updateDatabase({updatedDatabase}) {
    try {
        loadingMessage('Updating database...', 0);
        const res = yield http.put(`/databases`, updatedDatabase);
        successMessage('Database updated');
        yield put(databaseActions.updateDatabaseSuccess(res.data.msg, res.data.data));

    } catch (error) {
        yield put(databaseActions.updateDatabaseFailure(error.response.data));
        errorMessage("Couldn't update database");
    }
}

function* watchUpdateDatabase() {
    yield takeLatest(actionTypes.UPDATE_DATABASE_REQUEST, updateDatabase)
}

export function* databaseSaga() {
    yield all([
        watchGetDatabaseList(),
        watchFetchDatabase(),
        watchAddDatabase(),
        watchUpdateDatabase(),
        watchDeleteDatabase()
    ])
}
