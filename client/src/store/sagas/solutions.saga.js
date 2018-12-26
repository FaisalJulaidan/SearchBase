import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {http} from "../../helpers";
import {solutionsActions} from "../actions";


function* getSolutionsData({assistantID}) {
    try {
        const res = yield http.get(`/admin/assistant/${assistantID}/solutionsData`);
        return yield put(solutionsActions.getSolutionsSuccess(res.data))
    } catch (error) {
        console.log(error);
        return yield put(solutionsActions.getSolutionsFailure(error.response.data));
    }

}

function* watchSolutionsRequests(){
    yield takeEvery(actionTypes.GET_SOLUTIONS_REQUEST, getSolutionsData)
}

export function* solutionsSaga() {
    yield all([
        watchSolutionsRequests()
    ])
}