import * as actionTypes from '../actions/actionTypes';
import {put, takeEvery, takeLatest, all} from 'redux-saga/effects'
import {databaseActions, flowActions} from "../actions";
import {http, successMessage, loadingMessage, errorMessage} from "../../helpers";


function* getDatabasesList() {
    try {
        loadingMessage('Loading databases list');
        const res = yield http.get(`/databases`);
        yield put(databaseActions.getDatabasesListSuccess(res.data.data));
    } catch (error) {
        console.log(error);
        const msg = "Couldn't load databases list";
        yield put(databaseActions.getDatabasesListFailure(msg));
        errorMessage(msg);

    }
}
function* watchGetDatabaseList() {
    yield takeLatest(actionTypes.GET_DATABASES_LIST_REQUEST, getDatabasesList)
}

// ==================================================================

function* fetchDatabase({databaseID, pageNumber}) {
    try {
        loadingMessage('Loading database...', 0);
        const res = yield http.get(`/databases/${databaseID}/page/${pageNumber ? pageNumber : 1}`);
        yield put(databaseActions.fetchDatabaseSuccess(res.data.msg, res.data.data));
        successMessage('Database loaded');
    } catch (error) {
        console.log(error);
        const msg = "Couldn't load database's content";
        yield put(databaseActions.fetchDatabaseFailure(msg));
        errorMessage(msg);

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
        yield put(databaseActions.uploadDatabaseSuccess(res.data.msg, res.data.data));
        successMessage('Database uploaded');

    } catch (error) {
        console.log(error);
        const msg = "Couldn't upload new database";
        yield put(databaseActions.uploadDatabaseFailure(msg));
        errorMessage(msg);
    }
}
function* watchAddDatabase() {
    yield takeLatest(actionTypes.UPLOAD_DATABASE_REQUEST, uploadDatabase)
}

// ==================================================================

function* deleteDatabase({databaseID}) {
    try {
        console.log(databaseID);
        loadingMessage('Deleting database...', 0);
        const res = yield http.delete(`/databases/${databaseID}`);
        successMessage('Database deleted');
        yield put(databaseActions.deleteDatabaseSuccess(res.data.msg, databaseID));

    } catch (error) {
        console.log(error);
        const msg = "Couldn't delete database";
        yield put(databaseActions.deleteDatabaseFailure(msg));
        errorMessage(msg);
    }
}
function* watchDeleteDatabase() {
    yield takeLatest(actionTypes.DELETE_DATABASE_REQUEST, deleteDatabase)
}

// ==================================================================

function* updateDatabase({data, databaseID}) {
    try {
        loadingMessage('Updating database...', 0);
        const res = yield http.put(`/databases/${databaseID}`, data);
        yield put(databaseActions.updateDatabaseSuccess(res.data.msg, res.data.data));
        yield put(databaseActions.getDatabasesList());
        successMessage('Database updated');

    } catch (error) {
        console.log(error);
        const msg = "Couldn't update database";
        yield put(databaseActions.updateDatabaseFailure(msg));
        errorMessage(msg);
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
