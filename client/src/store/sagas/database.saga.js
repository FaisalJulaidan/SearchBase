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
        yield errorMessage("Couldn't load databases list");

    }
}

function* watchGetDatabaseList() {
    yield takeLatest(actionTypes.GET_DATABASES_LIST_REQUEST, getDatabasesList)
}

function* fetchDatabase({databaseID}) {
    try {
        loadingMessage('Loading database...', 0);
        const res = yield http.get(`/databases/${databaseID}`);
        yield put(databaseActions.fetchDatabaseSuccess(res.data.msg, res.data.data));
        yield successMessage('Database loaded');
    } catch (error) {
        console.log(error);
        yield errorMessage("Couldn't load database");
        yield put(databaseActions.fetchDatabaseFailure(error.response.data));
    }
}

function* watchFetchDatabase() {
    yield takeLatest(actionTypes.FETCH_DATABASE_REQUEST, fetchDatabase)
}

function* uploadDatabase({newDatabase}) {
    try {
        yield loadingMessage('Uploading database...', 0);
        const res = yield http.post(`/databases`, newDatabase);

        yield successMessage('Database uploaded');
        yield put(databaseActions.uploadDatabaseSuccess(res.data.msg, res.data.data));

    } catch (error) {
        console.log(error);
        yield put(databaseActions.uploadDatabaseFailure(error.response.data));
        yield errorMessage("Couldn't upload database");
    }
}

function* watchAddDatabase() {
    yield takeLatest(actionTypes.UPLOAD_DATABASE_REQUEST, uploadDatabase)
}

export function* databaseSaga() {
    yield all([
        watchGetDatabaseList(),
        watchFetchDatabase(),
        watchAddDatabase()
    ])
}
