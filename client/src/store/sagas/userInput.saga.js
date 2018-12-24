import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {userInputActions} from "../actions";
import {http, alertSuccess, alertError} from "../../helpers";

function* fetchUserInputs({assistantID}) {
    try {
        const res = yield http.get(`/assistant/${assistantID}/userinput`);
        return yield put(userInputActions.fetchUserInputsSuccess(res.data.data))
    } catch (error) {
        console.log(error);
        return yield put(userInputActions.fetchUserInputsFailure(error));
    }
}

function* watchFetchUserInputs() {
    yield takeEvery(actionTypes.FETCH_USERINPUT_REQUEST, fetchUserInputs)
}

function* clearAllUserInputs({assistantID}) {
    try {
        const res = yield http.delete(`/assistant/${assistantID}/userinput`);
        yield put(userInputActions.clearAllUserInputsSuccess());
        return yield alertSuccess('Cleared Successfully', res.data.msg)
    } catch (error) {
        console.log(error);
        yield put(userInputActions.clearAllUserInputsFailure(error));
        return yield alertError('Error', "Sorry, we could'nt clear all the records!");

    }
}

function* watchClearAllUserInputs() {
    yield takeEvery(actionTypes.CLEAR_ALL_USERINPUT_REQUEST, clearAllUserInputs)
}


export function* userInputSaga() {
    yield all([
        watchFetchUserInputs(),
        watchClearAllUserInputs(),
    ])
}