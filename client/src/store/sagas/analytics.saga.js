import {all, put, takeEvery, takeLatest} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {analyticsActions} from "../actions";
import {destroyMessage, errorHandler, errorMessage, flow, http, loadingMessage, successMessage} from "helpers";
// import * as Sentry from '@sentry/browser';

function* fetchAnalytics({assistantID, split}) {
    try {
        const res = yield http.get(`/assistant/${assistantID}/analytics?split=${split}`);

        yield put(analyticsActions.fetchAnalyticsSuccess(res.data?.data));
    } catch (error) {
        console.error(error);
        const msg = "Couldn't fetch analytics";
        yield put(analyticsActions.fetchAnalyticsFailure(msg));
        errorMessage(msg);
    }

}

function* watchFetchAnalytics() {
    yield takeEvery(actionTypes.FETCH_ANALYTICS_REQUEST, fetchAnalytics)
}

export function* analyticsSaga() {
    yield all([
        watchFetchAnalytics(),
    ])
}
