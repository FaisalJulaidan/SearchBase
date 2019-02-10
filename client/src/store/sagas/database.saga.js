import * as actionTypes from '../actions/actionTypes';
import {put, takeEvery, takeLatest, all} from 'redux-saga/effects'
import {databaseActions} from "../actions";
import {http} from "../../helpers";
import {alertError, destroyMessage, loadingMessage} from "../../helpers/alert";


function* getDatabaseList() {
    try {
        loadingMessage('Loading databases list');
        debugger

        const res = yield http.get(`/databases`);

        yield put(databaseActions.getDatabasesListSuccess(res.response.data));

    } catch (error) {
        console.log(error);
        yield destroyMessage();
        yield alertError('Loading databases list Unsuccessful', error.response.data.msg);
        yield put(databaseActions.getDatabasesListFailure(error.response.data));
    }
}

function* watchGetDatabaseList() {
    yield takeLatest(actionTypes.GET_DATABASES_LIST_REQUEST, getDatabaseList)
}

function* addDatabase({newDatabase}) {
    try {
        loadingMessage('Loading databases list');
        // const res = yield http.get(`/databases/${companyID}`);

        // debugger;

        // yield put(databaseActions.getDatabasesListSuccess(res.response.data));

    } catch (error) {
        // console.log(error);
        // yield destroyMessage();
        // yield alertError('Loading databases list Unsuccessful', error.response.data.msg);
        // yield put(databaseActions.getDatabasesListFailure(error.response.data));
    }
}

function* watchAddDatabase() {
    yield takeLatest(actionTypes.UPLOAD_DATABASE_REQUEST, addDatabase)
}

export function* databaseSaga() {
    yield all([
        watchGetDatabaseList(),
        watchAddDatabase()
    ])
}
