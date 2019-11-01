import {all, put, takeEvery} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {paymentActions} from "../actions";
import {errorMessage, http} from "helpers";

function* generateCheckoutSession({companyID,plan}) {
    try {
        const res = yield http.post(`/pricing/genCheckoutURL`, {companyID,plan});
        yield put(paymentActions.generateCheckoutSessionSuccess(res.data?.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't generate checkout";
        yield put(paymentActions.generateCheckoutSessionFailure(msg));
        errorMessage(msg);
    }

}

function* watchGenerateCheckoutSession() {
    yield takeEvery(actionTypes.GENERATE_CHECKOUT_SESSION_REQUEST, generateCheckoutSession)
}

export function* paymentSaga() {
    yield all([
        watchGenerateCheckoutSession(),
    ])
}