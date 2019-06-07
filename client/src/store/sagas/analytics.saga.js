import {all, put, takeEvery} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {analyticsActions} from "../actions";
import {errorMessage, http} from "helpers";

// import * as Sentry from '@sentry/browser';

function* fetchAnalytics({assistantID}) {
    try {
        const res = yield http.get(`/assistant/${assistantID}/analytics`);
        yield put(analyticsActions.fetchAnalyticsSuccess(res.data?.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't fetch analytics";
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
