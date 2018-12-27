import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {http} from "../../helpers";
import {solutionsActions} from "../actions";


function* getSolutionsData({assistantID}) {
    try {
        const res = yield http.get(`/assistant/${assistantID}/solutionsData`);
        return yield put(solutionsActions.getSolutionsSuccess(res.data))
    } catch (error) {
        console.log(error);
        return yield put(solutionsActions.getSolutionsFailure(error.response.data));
    }

}

function* addSolution({assistantID, solution}) {
    try {
        const res = yield http.put(`/assistant/${assistantID}/solutionsData`, solution);
        yield put(solutionsActions.addSolutionSuccess(res.message))
        return getSolutionsData({assistantID})
    } catch (error) {
        console.log(error);
        return yield put(solutionsActions.addSolutionFailure(error.response.data));
    }

}

function* watchSolutionsRequests(){
    yield takeEvery(actionTypes.GET_SOLUTIONS_REQUEST, getSolutionsData)
}

function* watchAddSolutionRequests(){
    yield takeEvery(actionTypes.ADD_SOLUTION_REQUEST, addSolution)
}

export function* solutionsSaga() {
    yield all([
        watchSolutionsRequests(),
        watchAddSolutionRequests()
    ])
}