import {all, put, takeEvery, takeLatest} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {analyticsActions} from "../actions";
import {destroyMessage, errorHandler, errorMessage, flow, http, loadingMessage, successMessage} from "helpers";
import * as Sentry from '@sentry/browser';

function* fetchAnalytics({assistantID}) {
    try {
        const res = yield http.get(`/assistants/`);
        yield put(crmActions.getConnectedCRMs());

        if (!res.data?.data)
            throw Error(`Can't fetch assistants`);

        yield put(assistantActions.fetchAssistantsSuccess(res.data?.data));
    } catch (error) {
        console.error(error);
        const msg = "Couldn't load assistants";
        yield put(assistantActions.fetchAssistantsFailure(msg));
        errorMessage(msg);
    }

}
