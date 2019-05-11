import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {integrationsActions} from "../actions";
import {http, errorMessage} from "helpers";


function* fetchCRMs() {
    try {
        const res = yield http.get(`/crm`);
        if (!res.data?.data)
            throw Error(`Can't fetch CRMs`);

        yield put(integrationsActions.getConnectedCRMsSuccess(res.data?.data));
    } catch (error) {
        console.error(error);
        const msg = "Couldn't load CRMs";
        yield put(integrationsActions.getConnectedCRMsFailure(msg));
        errorMessage(msg);
    }

}


function* watchFetchCRMs() {
    yield takeEvery(actionTypes.GET_CONNECTED_CRMS_REQUEST, fetchCRMs)
}


export function* integrationsSaga() {
    yield all([
        watchFetchCRMs(),
    ])
}
